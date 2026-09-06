// tend-windows@tend — the window list, published from inside the shell (card:canvas-windows.md).
//
// GNOME 50.1 refuses `org.gnome.Shell.Introspect.GetWindows` to a caller
// that is not on its allow-list (measured from Henri's shell, 2026-09-06),
// and the fence has no session bus at all; so the list is readable only
// from inside the shell's own process, and this is the few lines that
// read it there.  One D-Bus name, one method, one signal:
//
//     org.tend.Windows            at /org/tend/Windows
//       List() -> s               the windows as a JSON array of
//                                 {id, seq, app, title, focus, x, y, w, h, at}
//       Changed()                 something in that list changed; call List
//
// `at` is the epoch second of the window's last change this extension saw
// (created, retitled, moved, resized, focused) — the compositor keeps no
// wall clock for that, so the extension keeps one.  Windows the shell
// hides from the taskbar (docks, popups, the shell's own) are left out.
//
// It reads the desk and changes nothing on it: no window is moved, closed
// or focused from here, and nothing inside the fence can reach this —
// the mirror is `tools/windows.py`, on the person's side, and a session
// sees files.  Installed by his hand (`tools/windows.py --install`, then
// a log-out and `gnome-extensions enable tend-windows@tend`); code in
// the compositor's process is a size he accepted on the card.

import Gio from 'gi://Gio';
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

const WINDOW_SIGNALS = ['notify::title', 'position-changed', 'size-changed', 'focus', 'unmanaged'];

function now() {
    return Math.floor(Date.now() / 1000);
}

export default class TendWindows extends Extension {
    enable() {
        this._at = new Map();          // window -> epoch of its last change seen here
        this._handlers = new Map();    // window -> [signal ids]
        this._dbus = Gio.DBusExportedObject.wrapJSObject(IFACE, this);
        this._dbus.export(Gio.DBus.session, OBJECT_PATH);
        this._owner = Gio.bus_own_name(Gio.BusType.SESSION, BUS_NAME, Gio.BusNameOwnerFlags.NONE,
            null, null, null);
        const display = global.display;
        this._displayHandlers = [
            display.connect('window-created', (_d, w) => this._watch(w)),
            display.connect('notify::focus-window', () => this._changed(display.focus_window)),
        ];
        for (const actor of global.get_window_actors())
            this._watch(actor.meta_window);
    }

    disable() {
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
        if (this._owner) {
            Gio.bus_unown_name(this._owner);
            this._owner = 0;
        }
        if (this._dbus) {
            this._dbus.unexport();
            this._dbus = null;
        }
    }

    _watch(w) {
        if (!w || this._handlers.has(w))
            return;
        const ids = WINDOW_SIGNALS.map(name => w.connect(name, () => {
            if (name === 'unmanaged')
                this._forget(w);
            else
                this._changed(w);
        }));
        this._handlers.set(w, ids);
        this._at.set(w, now());
        this._signal();
    }

    _forget(w) {
        const ids = this._handlers.get(w) ?? [];
        for (const id of ids) {
            try { w.disconnect(id); } catch (_e) { /* already gone */ }
        }
        this._handlers.delete(w);
        this._at.delete(w);
        this._signal();
    }

    _changed(w) {
        if (w && this._at.has(w))
            this._at.set(w, now());
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
            });
        }
        return JSON.stringify(rows);
    }
}
