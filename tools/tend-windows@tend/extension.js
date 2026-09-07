// tend-windows@tend — the canvas placed on the screen, from inside the shell (card:canvas-windows.md).
//
// Henri's chain, 2026-09-06 (spec/canvas.md): the user's command creates a
// file in canvas/ → the window opens where the file says → a move changes
// the file → after a shutdown the windows come back where they were →
// closing the window removes the file.  This is the placing hand for that
// chain on GNOME 50: GNOME refuses the window list to a plain caller
// (measured 2026-09-06), so the hand runs inside the shell's own process,
// which is a size he accepted.
//
//     ~/.local/state/tend/canvas/<name>.win      one file, one window
//         run tools/panel.py                     what runs in it (a shell line)
//         dir /home/henri/tend                   where it runs
//         frame X Y W H                          where the window is — written back from here
//         at EPOCH                               the last change seen here
//
// A `.win` with a `run` line and no window of its own is started in a
// terminal whose title says which file it is — `ptyxis --title=tend:NAME
// -- sh -c RUN` — and **the window whose title begins `tend:NAME` is the
// file's window**: the tend interface at its smallest.  A window with no
// such title is a legacy window and nothing here touches it.  The window
// goes to the file's `frame`, or the layout rule places it (a cascade)
// when the file gives none; a move or resize writes the frame back; a
// `frame` edited by hand moves the window; the window closed from its X
// removes the file; the file removed closes the window.  Windows going
// down with the shell are not closed: after `disable` no file is removed.
//
// The list stays published for a reader — org.tend.Windows at
// /org/tend/Windows, `List() -> s` (JSON rows: id, seq, app, title,
// focus, x, y, w, h, at, file) and `Changed` — so `tools/windows.py
// --list` and `--check` can see the desk from his shell.  Nothing inside
// the fence can reach this; a session sees files.

import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Meta from 'gi://Meta';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

const BUS_NAME = 'org.tend.Windows';
const OBJECT_PATH = '/org/tend/Windows';
const IFACE = `
<node>
  <interface name="org.tend.Windows">
    <method name="List">
      <arg type="s" direction="out" name="json"/>
    </method>
    <signal name="Changed"/>
  </interface>
</node>`;

const TITLE = 'tend:';                 // a window says which file it is: its title begins `tend:NAME`
const SUFFIX = '.win';
const CANVAS = GLib.build_filenamev([GLib.get_home_dir(), '.local', 'state', 'tend', 'canvas']);
const TERMINAL = ['ptyxis'];           // `--title=tend:NAME -- sh -c RUN`; a `--` command is its own instance
const CASCADE = 40;                    // the layout rule: each new window forty pixels on from the last
const CASCADE_W = 1000, CASCADE_H = 700;
const RELAUNCH_AFTER = 15;             // seconds before a started file with no window yet is started again
const WINDOW_SIGNALS = ['notify::title', 'position-changed', 'size-changed', 'focus', 'unmanaged'];

function now() {
    return Math.floor(Date.now() / 1000);
}

function log(msg) {
    console.log(`tend-windows: ${msg}`);
}

function decode(bytes) {
    return new TextDecoder().decode(bytes);
}

// The file, read: {run, dir, frame: [x, y, w, h] | null, lines}; null when it cannot be read.
function readWin(path) {
    let bytes;
    try {
        [, bytes] = GLib.file_get_contents(path);
    } catch (_e) {
        return null;
    }
    const lines = decode(bytes).split('\n');
    const got = {run: '', dir: '', frame: null, lines};
    for (const line of lines) {
        if (!line.trim() || line.startsWith('#'))
            continue;
        const i = line.indexOf(' ');
        const key = i < 0 ? line : line.slice(0, i);
        const value = i < 0 ? '' : line.slice(i + 1).trim();
        if (key === 'run')
            got.run = value;
        else if (key === 'dir')
            got.dir = value;
        else if (key === 'frame') {
            const n = value.split(/\s+/).map(Number);
            if (n.length === 4 && n.every(Number.isInteger))
                got.frame = n;
        }
    }
    return got;
}

// The frame and the time into the file, the other lines kept as they are.
function writeFrame(path, rect) {
    const info = readWin(path);
    if (!info)
        return;
    const kept = info.lines.filter(l => !(l.startsWith('frame ') || l.startsWith('at ') || l.trim() === ''));
    kept.push(`frame ${rect.x} ${rect.y} ${rect.width} ${rect.height}`, `at ${now()}`);
    try {
        GLib.file_set_contents(path, kept.join('\n') + '\n');
    } catch (e) {
        log(`cannot write ${path}: ${e.message}`);
    }
}

function fileName(w) {
    const title = w?.get_title?.() || '';
    if (!title.startsWith(TITLE))
        return null;
    const name = title.slice(TITLE.length).split(/\s/)[0];
    return name || null;
}

function sameFrame(rect, frame) {
    return !!frame && rect.x === frame[0] && rect.y === frame[1] && rect.width === frame[2] && rect.height === frame[3];
}

function sameFrames(a, b) {
    return !!a && !!b && a.length === 4 && a.every((v, i) => v === b[i]);
}

// The command line the window runs: the title said twice — the terminal's flag,
// and the OSC the program's shell prints before it — so that a terminal which
// drops the flag beside a command still names its file.
function commandFor(name, run) {
    return ['sh', '-c', `printf '\\033]0;${TITLE}${name}\\a'; ${run}`];
}

export default class TendWindows extends Extension {
    enable() {
        this._closing = false;
        this._at = new Map();          // window -> epoch of its last change seen here
        this._handlers = new Map();    // window -> [signal ids]
        this._files = new Map();       // name -> {path, window, started, frame}
        this._byWindow = new Map();    // window -> name
        this._placed = 0;
        this._dbus = Gio.DBusExportedObject.wrapJSObject(IFACE, this);
        this._dbus.export(Gio.DBus.session, OBJECT_PATH);
        this._owner = Gio.bus_own_name(Gio.BusType.SESSION, BUS_NAME, Gio.BusNameOwnerFlags.NONE,
            null, null, null);
        const display = global.display;
        this._displayHandlers = [
            display.connect('window-created', (_d, w) => this._watch(w)),
            display.connect('notify::focus-window', () => this._changed(display.focus_window)),
        ];
        try {
            this._displayHandlers.push(display.connect('closing', () => { this._closing = true; }));
        } catch (e) {
            log(`no closing signal on the display (${e.message}) — disable is the only guard against a shutdown reading as closes`);
        }
        for (const actor of global.get_window_actors())
            this._watch(actor.meta_window);
        // the canvas: every file now, and every change after
        GLib.mkdir_with_parents(CANVAS, 0o755);
        this._dir = Gio.File.new_for_path(CANVAS);
        try {
            this._monitor = this._dir.monitor_directory(Gio.FileMonitorFlags.WATCH_MOVES, null);
            this._monitor.connect('changed', (_m, file, other, event) => this._onFile(file, other, event));
        } catch (e) {
            log(`cannot watch ${CANVAS}: ${e.message}`);
            this._monitor = null;
        }
        let names = [];
        try {
            const it = this._dir.enumerate_children('standard::name', Gio.FileQueryInfoFlags.NONE, null);
            let info;
            while ((info = it.next_file(null)) !== null)
                names.push(info.get_name());
        } catch (e) {
            log(`cannot read ${CANVAS}: ${e.message}`);
        }
        for (const name of names.sort())
            if (name.endsWith(SUFFIX))
                this._take(GLib.build_filenamev([CANVAS, name]));
    }

    disable() {
        // first: from here on a window going away is the shell going down, never a close
        this._closing = true;
        if (this._monitor) {
            this._monitor.cancel();
            this._monitor = null;
        }
        for (const id of this._displayHandlers ?? [])
            global.display.disconnect(id);
        this._displayHandlers = null;
        for (const [w, ids] of this._handlers ?? []) {
            for (const id of ids) {
                try { w.disconnect(id); } catch (_e) { /* the window is already gone */ }
            }
        }
        this._handlers = null;
        this._at = null;
        this._files = null;
        this._byWindow = null;
        if (this._owner) {
            Gio.bus_unown_name(this._owner);
            this._owner = 0;
        }
        if (this._dbus) {
            this._dbus.unexport();
            this._dbus = null;
        }
    }

    // --- the canvas side ---

    _onFile(file, other, event) {
        const E = Gio.FileMonitorEvent;
        const isWin = f => f && (f.get_basename() || '').endsWith(SUFFIX);
        if (event === E.RENAMED) {
            if (isWin(file))
                this._drop(file.get_basename().slice(0, -SUFFIX.length));
            if (isWin(other))
                this._take(other.get_path());
            return;
        }
        if (!isWin(file))
            return;
        if (event === E.CREATED || event === E.CHANGED || event === E.CHANGES_DONE_HINT || event === E.MOVED_IN)
            this._take(file.get_path());
        else if (event === E.DELETED || event === E.MOVED_OUT)
            this._drop(file.get_basename().slice(0, -SUFFIX.length));
    }

    // A file, now: bind its window if one is on the desk, move it if the frame changed, else start it.
    _take(path) {
        const name = GLib.path_get_basename(path).slice(0, -SUFFIX.length);
        const info = readWin(path);
        if (!info)
            return;                        // gone between the event and the read
        if (!info.run) {
            if (!this._files.has(name))
                log(`${name}${SUFFIX}: no run line — not started (a file of the old mirror's? rm it)`);
            return;
        }
        let entry = this._files.get(name);
        if (!entry) {
            entry = {path, window: null, started: 0, frame: null};
            this._files.set(name, entry);
        }
        entry.path = path;
        if (entry.window) {
            // a frame that differs from the one written from here is a hand's edit: move the window.
            // (Not "differs from the window": during a drag the file holds the last write-back and
            // the window has moved on, and reading that back would fight the hand on the window.)
            if (info.frame && !sameFrames(info.frame, entry.frame)) {
                entry.frame = info.frame;
                entry.window.move_resize_frame(true, ...info.frame);
            }
            return;
        }
        entry.frame = info.frame;
        for (const actor of global.get_window_actors()) {
            if (fileName(actor.meta_window) === name) {
                this._bind(name, actor.meta_window);
                return;
            }
        }
        if (entry.started && now() - entry.started < RELAUNCH_AFTER)
            return;                        // started, not up yet
        entry.started = now();
        const argv = [...TERMINAL, `--title=${TITLE}${name}`, '--', ...commandFor(name, info.run)];
        try {
            GLib.spawn_async(info.dir || null, argv, null, GLib.SpawnFlags.SEARCH_PATH, null);
            log(`${name}: started ${info.run}`);
        } catch (e) {
            log(`${name}: cannot start ${argv[0]}: ${e.message}`);
        }
    }

    // The file is gone: its window goes with it (his 17:35: the X and rm are the same act).
    _drop(name) {
        const entry = this._files.get(name);
        if (!entry)
            return;
        this._files.delete(name);
        if (entry.window) {
            this._byWindow.delete(entry.window);
            try {
                entry.window.delete(global.get_current_time());
            } catch (_e) { /* already gone */ }
            log(`${name}: file removed, window closed`);
        }
    }

    // --- the desk side ---

    _match(w) {
        if (!w || this._byWindow.has(w))
            return;
        const name = fileName(w);
        if (!name)
            return;
        const entry = this._files.get(name);
        if (!entry || (entry.window && entry.window !== w))
            return;                        // no file of that name — or one file, one window, and it has one
        this._bind(name, w);
    }

    _bind(name, w) {
        const entry = this._files.get(name);
        entry.window = w;
        this._byWindow.set(w, name);
        let frame = entry.frame;
        if (!frame) {
            const n = this._placed++;
            frame = [CASCADE + CASCADE * n, CASCADE + CASCADE * n, CASCADE_W, CASCADE_H];
        }
        entry.frame = frame;
        w.move_resize_frame(true, ...frame);
        writeFrame(entry.path, {x: frame[0], y: frame[1], width: frame[2], height: frame[3]});
        log(`${name}: placed at ${frame.join(' ')}`);
    }

    _watch(w) {
        if (!w || this._handlers.has(w))
            return;
        const ids = WINDOW_SIGNALS.map(name => w.connect(name, () => {
            if (name === 'unmanaged')
                this._forget(w);
            else
                this._changed(w, name);
        }));
        this._handlers.set(w, ids);
        this._at.set(w, now());
        this._match(w);
        this._signal();
    }

    _forget(w) {
        const ids = this._handlers.get(w) ?? [];
        for (const id of ids) {
            try { w.disconnect(id); } catch (_e) { /* already gone */ }
        }
        this._handlers.delete(w);
        this._at.delete(w);
        const name = this._byWindow.get(w);
        if (name !== undefined) {
            this._byWindow.delete(w);
            const entry = this._files.get(name);
            if (entry && entry.window === w) {
                entry.window = null;
                if (!this._closing) {
                    // closed from its X: the file goes (his 17:35).  Going down with the shell is not a close.
                    this._files.delete(name);
                    try {
                        Gio.File.new_for_path(entry.path).delete(null);
                        log(`${name}: window closed, file removed`);
                    } catch (e) {
                        log(`${name}: window closed, cannot remove ${entry.path}: ${e.message}`);
                    }
                }
            }
        }
        this._signal();
    }

    _changed(w, what) {
        if (w && this._at.has(w))
            this._at.set(w, now());
        if (what === 'notify::title')
            this._match(w);                // the terminal sets its title after the window exists
        if (w && (what === 'position-changed' || what === 'size-changed')) {
            const name = this._byWindow.get(w);
            const entry = name === undefined ? null : this._files.get(name);
            if (entry) {
                const r = w.get_frame_rect();
                if (!sameFrame(r, entry.frame)) {
                    entry.frame = [r.x, r.y, r.width, r.height];
                    writeFrame(entry.path, r);
                }
            }
        }
        this._signal();
    }

    _signal() {
        if (this._dbus)
            this._dbus.emit_signal('Changed', null);
    }

    List() {
        const focus = global.display.focus_window;
        const rows = [];
        for (const actor of global.get_window_actors()) {
            const w = actor.meta_window;
            if (!w || w.is_skip_taskbar() || w.get_window_type() !== Meta.WindowType.NORMAL)
                continue;
            const r = w.get_frame_rect();
            rows.push({
                id: Number(w.get_id()),
                seq: w.get_stable_sequence(),
                app: w.get_gtk_application_id() || w.get_wm_class() || '',
                title: w.get_title() || '',
                focus: w === focus,
                x: r.x, y: r.y, w: r.width, h: r.height,
                at: this._at.get(w) ?? now(),
                file: this._byWindow.get(w) ?? '',
            });
        }
        return JSON.stringify(rows);
    }
}
