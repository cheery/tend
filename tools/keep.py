#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-25 — "go with A" (board/keep.md; the reusable launcher, not the node confining itself)
"""tools/keep.py — run a program able to read only what it was handed.

    tools/keep.py [--allow PATH]... -- program args...

A launcher, and the grant is the launcher's, not the program's — the
boundary is set from outside the thing bounded (board/keep.md, and the
tree's Rule 1: a party may not bound itself).  It builds a Landlock
ruleset that governs filesystem *reads*, grants read on the paths named
with --allow (plus the system roots any program needs to run at all),
restricts itself irreversibly, then execs the program.  Inside, the
program reads what it was given and gets EACCES on the file beside it.

  first slice, said plainly: this scopes filesystem *reads* only — a
  program is blind to data it was not handed, which is exactly problem 1
  ("how are users' data protected from programs?").  Write-scoping and
  network are handled bits Landlock also has and this does not set yet;
  they are later turns, named here so the gap is not silent.

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


class path_beneath_attr(ctypes.Structure):
    _pack_ = 1  # struct is __attribute__((packed)): u64 then s32, size 12
    _fields_ = [("allowed_access", ctypes.c_uint64),
                ("parent_fd", ctypes.c_int32)]


def _fail(msg, code=1):
    sys.stderr.write("keep: " + msg + "\n")
    sys.exit(code)


def confine(allow):
    attr = ruleset_attr(HANDLED)
    fd = libc.syscall(NR_create_ruleset, ctypes.byref(attr),
                      ctypes.sizeof(attr), 0)
    if fd < 0:
        e = ctypes.get_errno()
        _fail(f"Landlock is not available ({os.strerror(e)}) — refusing to "
              f"run the program unconfined.  A grant that became 'everything' "
              f"silently is the one lie keep must not tell.")

    granted = 0
    for path in SYSTEM_READ + list(allow):
        try:
            pfd = os.open(path, os.O_PATH | os.O_CLOEXEC)
        except FileNotFoundError:
            if path in SYSTEM_READ:
                continue  # a root this machine does not have
            _fail(f"nothing to grant at {path!r} — it does not exist.")
        try:
            isdir = os.path.isdir(path)
            allowed = HANDLED if isdir else FS_READ_FILE
            pb = path_beneath_attr(allowed, pfd)
            r = libc.syscall(NR_add_rule, fd, LANDLOCK_RULE_PATH_BENEATH,
                             ctypes.byref(pb), 0)
            if r != 0:
                _fail(f"could not grant {path!r}: {os.strerror(ctypes.get_errno())}")
            granted += 1
        finally:
            os.close(pfd)

    if libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        _fail(f"no_new_privs: {os.strerror(ctypes.get_errno())}")
    if libc.syscall(NR_restrict_self, fd, 0) != 0:
        _fail(f"restrict_self: {os.strerror(ctypes.get_errno())}")
    os.close(fd)


def main(argv):
    allow, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--allow":
            if i + 1 >= len(argv):
                _fail("--allow needs a path", 2)
            allow.append(argv[i + 1]); i += 2
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
        _fail("nothing to run — tools/keep.py [--allow PATH]... -- program args", 2)
    confine(allow)
    try:
        os.execvp(prog[0], prog)
    except OSError as e:
        _fail(f"cannot exec {prog[0]!r}: {e.strerror}", 127)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
