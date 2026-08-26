#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-25 — "go with A" (board/keep.md; the reusable launcher, not the node confining itself)
"""tools/keep.py — run a program able to read only what it was handed.

    tools/keep.py [--allow PATH]... [--write PATH]... [--no-net] -- program args...

A launcher, and the grant is the launcher's, not the program's — the
boundary is set from outside the thing bounded (board/keep.md, and the
tree's Rule 1: a party may not bound itself).  It builds a Landlock
ruleset that governs filesystem *reads*, grants read on the paths named
with --allow (plus the system roots any program needs to run at all),
restricts itself irreversibly, then execs the program.  Inside, the
program reads what it was given and gets EACCES on the file beside it.

  reads, always: --allow grants read beneath a path; a program is blind
  to data it was not handed, which is exactly problem 1 ("how are users'
  data protected from programs?").

  writes, opt-in: --write grants read+write beneath a path, and turns on
  the write boundary — with at least one --write the program may change
  only what it was handed writable, and is refused everywhere else,
  including paths it can read.  With no --write, keep governs reads only
  and a program writes where the fence allows; that default is stated,
  not silent.

  network, opt-in: --no-net turns on the TCP boundary with nothing
  granted through it — the program can neither connect nor bind a TCP
  socket, on any port (measured 2026-08-26: EACCES on connect, on bind,
  and on bind to port 0; UNIX sockets are not TCP and stay as they were).
  Needs Landlock ABI 4; asked for on an older kernel, keep refuses rather
  than run the program with a network it was told to take away.  With no
  --no-net, a program has whatever network the fence left it; that
  default is stated, not silent.  Per-port grants are the turn after
  this one, for when a program needs a port — none does yet.

  never silent (Rule 9): if Landlock is not available, keep does NOT run
  the program unconfined — it refuses, loudly, because a grant that
  silently became "everything" is the one lie this must not tell.

  the grant only narrows: Landlock rules add nothing a path did not
  already allow, and restrict_self is one-way, so the program cannot
  widen what keep gave it (Rule 2, applied to a program).

No build, no privilege: Landlock is an unprivileged LSM, reached here
through the raw syscalls with ctypes.  Measured available on this
machine at ABI 4, from inside the fence (board/keep.md).
"""
import ctypes
import os
import sys

# x86_64 syscall numbers; Landlock is arch-stable but the numbers are not,
# so a port names them here rather than hiding the assumption.
NR_create_ruleset = 444
NR_add_rule = 445
NR_restrict_self = 446
PR_SET_NO_NEW_PRIVS = 38
LANDLOCK_RULE_PATH_BENEATH = 1

# The read accesses keep governs.  EXECUTE and the write/make bits are
# left unhandled, so they stay as the fence already left them; what this
# tool decides is who may *read* what.
FS_READ_FILE = 1 << 2
FS_READ_DIR = 1 << 3
HANDLED = FS_READ_FILE | FS_READ_DIR

# The write accesses `--write` governs: everything that changes a name
# or a file's contents beneath a granted directory.  All ABI 1 except
# TRUNCATE (ABI 3), which confine() adds only when the kernel offers it
# — a handled bit the kernel does not know makes create_ruleset refuse
# the whole ruleset.
FS_WRITE_FILE = 1 << 1
FS_REMOVE_DIR = 1 << 4
FS_REMOVE_FILE = 1 << 5
FS_MAKE_CHAR = 1 << 6
FS_MAKE_DIR = 1 << 7
FS_MAKE_REG = 1 << 8
FS_MAKE_SOCK = 1 << 9
FS_MAKE_FIFO = 1 << 10
FS_MAKE_BLOCK = 1 << 11
FS_MAKE_SYM = 1 << 12
FS_TRUNCATE = 1 << 14
WRITE_HANDLED = (FS_WRITE_FILE | FS_REMOVE_DIR | FS_REMOVE_FILE
                 | FS_MAKE_CHAR | FS_MAKE_DIR | FS_MAKE_REG | FS_MAKE_SOCK
                 | FS_MAKE_FIFO | FS_MAKE_BLOCK | FS_MAKE_SYM)
LANDLOCK_CREATE_RULESET_VERSION = 1 << 0

# The network accesses `--no-net` governs (ABI 4): both TCP bits, handled
# with no port rule beneath them, which is "no TCP at all".  Landlock has
# no UDP or UNIX-socket bits, so those are outside what keep can say.
NET_BIND_TCP = 1 << 0
NET_CONNECT_TCP = 1 << 1
NET_HANDLED = NET_BIND_TCP | NET_CONNECT_TCP

# The roots any program needs just to run — the interpreter, the shared
# libraries, the loader cache, /proc and /dev.  These are the machine,
# not the person's data, so granting read on them is the honest baseline
# every grant sits on.  (Inside the fence /bin, /lib* are symlinks into
# /usr, already covered; on a bare host they are real, so both are named
# and the ones that exist are granted.)
SYSTEM_READ = ["/usr", "/etc", "/lib", "/lib64", "/bin", "/sbin",
               "/proc", "/dev"]

libc = ctypes.CDLL(None, use_errno=True)
libc.syscall.restype = ctypes.c_long


class ruleset_attr(ctypes.Structure):
    # v1 attr: filesystem only, size 8 — accepted on every Landlock ABI.
    _fields_ = [("handled_access_fs", ctypes.c_uint64)]


class ruleset_attr_v4(ctypes.Structure):
    # v4 attr adds the network field, size 16 — used only when --no-net
    # asks for it, so a kernel below ABI 4 never sees a size it rejects.
    _fields_ = [("handled_access_fs", ctypes.c_uint64),
                ("handled_access_net", ctypes.c_uint64)]


class path_beneath_attr(ctypes.Structure):
    _pack_ = 1  # struct is __attribute__((packed)): u64 then s32, size 12
    _fields_ = [("allowed_access", ctypes.c_uint64),
                ("parent_fd", ctypes.c_int32)]


def _fail(msg, code=1):
    sys.stderr.write("keep: " + msg + "\n")
    sys.exit(code)


def landlock_abi():
    """The kernel's Landlock ABI version, or 0 if unavailable — used to
    mask write bits the running kernel does not know."""
    v = libc.syscall(NR_create_ruleset, 0, 0, LANDLOCK_CREATE_RULESET_VERSION)
    return v if v > 0 else 0


def confine(read_allow, write_allow, no_net=False):
    abiv = landlock_abi()
    write_bits = 0
    handled = HANDLED
    if write_allow:
        write_bits = WRITE_HANDLED | (FS_TRUNCATE if abiv >= 3 else 0)
        handled |= write_bits
    if no_net:
        if abiv < 4:
            _fail(f"--no-net needs Landlock ABI 4 and this kernel offers "
                  f"{abiv} — refusing to run the program with the network it "
                  f"was told to lose.")
        attr = ruleset_attr_v4(handled, NET_HANDLED)
    else:
        attr = ruleset_attr(handled)
    fd = libc.syscall(NR_create_ruleset, ctypes.byref(attr),
                      ctypes.sizeof(attr), 0)
    if fd < 0:
        e = ctypes.get_errno()
        _fail(f"Landlock is not available ({os.strerror(e)}) — refusing to "
              f"run the program unconfined.  A grant that became 'everything' "
              f"silently is the one lie keep must not tell.")

    # read-only grants first, then the writable ones; a writable file may
    # be opened for writing and truncated, a writable dir may also have
    # names made and removed beneath it.
    file_write = FS_READ_FILE | FS_WRITE_FILE | (FS_TRUNCATE if abiv >= 3 else 0)
    plan = ([(p, False) for p in SYSTEM_READ + list(read_allow)]
            + [(p, True) for p in write_allow])
    for path, writable in plan:
        try:
            pfd = os.open(path, os.O_PATH | os.O_CLOEXEC)
        except FileNotFoundError:
            if path in SYSTEM_READ:
                continue  # a root this machine does not have
            _fail(f"nothing to grant at {path!r} — it does not exist.")
        try:
            isdir = os.path.isdir(path)
            if writable:
                allowed = (FS_READ_FILE | FS_READ_DIR | write_bits) if isdir else file_write
            else:
                allowed = (FS_READ_FILE | FS_READ_DIR) if isdir else FS_READ_FILE
            allowed &= handled  # a rule may never grant past what is handled
            pb = path_beneath_attr(allowed, pfd)
            r = libc.syscall(NR_add_rule, fd, LANDLOCK_RULE_PATH_BENEATH,
                             ctypes.byref(pb), 0)
            if r != 0:
                _fail(f"could not grant {path!r}: {os.strerror(ctypes.get_errno())}")
        finally:
            os.close(pfd)

    if libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        _fail(f"no_new_privs: {os.strerror(ctypes.get_errno())}")
    if libc.syscall(NR_restrict_self, fd, 0) != 0:
        _fail(f"restrict_self: {os.strerror(ctypes.get_errno())}")
    os.close(fd)


def main(argv):
    allow, write, no_net, i = [], [], False, 0
    while i < len(argv):
        a = argv[i]
        if a == "--allow":
            if i + 1 >= len(argv):
                _fail("--allow needs a path", 2)
            allow.append(argv[i + 1]); i += 2
        elif a == "--write":
            if i + 1 >= len(argv):
                _fail("--write needs a path", 2)
            write.append(argv[i + 1]); i += 2
        elif a == "--no-net":
            no_net = True; i += 1
        elif a == "--":
            i += 1; break
        elif a in ("-h", "--help"):
            sys.stdout.write(__doc__); return 0
        elif a.startswith("-"):
            _fail(f"unknown argument `{a}`", 2)
        else:
            break
    prog = argv[i:]
    if not prog:
        _fail("nothing to run — tools/keep.py [--allow PATH]... [--write PATH]... [--no-net] -- program args", 2)
    confine(allow, write, no_net)
    try:
        os.execvp(prog[0], prog)
    except OSError as e:
        _fail(f"cannot exec {prog[0]!r}: {e.strerror}", 127)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
