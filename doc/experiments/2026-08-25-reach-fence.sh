#!/bin/sh
# The fence the reach experiment ran under (doc/experiments/2026-08-25-reach.md).
# Not a tool: a record.  System read-only, an empty home, no network, this
# project the one writable thing.  Borrowed from ~/gestate/tools/sandbox.sh.
P=/home/cheery/tend
exec bwrap --unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-net --die-with-parent --new-session \
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin \
  --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --tmpfs "$HOME" \
  --bind "$P" "$P" --chdir "$P" \
  --setenv HOME "$HOME" --setenv TEND_FENCED 1 \
  --setenv PATH "$P/.venv/bin:/usr/local/bin:/usr/bin:/bin" \
  --unsetenv SSH_AUTH_SOCK --unsetenv ANTHROPIC_API_KEY --unsetenv DBUS_SESSION_BUS_ADDRESS \
  -- "$@"
