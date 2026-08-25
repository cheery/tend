#!/bin/sh
# The sessions-first trial's fence (doc/experiments/2026-08-25-both.md).
# Not a tool: a record.  The reach fence of 2026-08-25-reach-fence.sh, plus
# the two rows the reach table said a session cannot do without: the
# state directory passed through read-write (the sitting clock, the leash
# ledger, the kaizen want), and one named tree read-only (gestate, so its
# audit can reach tend).  DISPLAY scrubbed, since the display row is off.
P=/home/cheery/tend
RT=/run/user/$(id -u)
exec bwrap --unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-net --die-with-parent --new-session \
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin \
  --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --tmpfs "$HOME" \
  --bind "$P" "$P" --chdir "$P" \
  --bind "$HOME/.local/state" "$HOME/.local/state" \
  --dir "$RT" --bind-try "$RT/gestate-sitting-$(id -u)" "$RT/gestate-sitting-$(id -u)" \
  --ro-bind /home/cheery/gestate /home/cheery/gestate \
  --setenv HOME "$HOME" --setenv XDG_RUNTIME_DIR "$RT" --setenv TEND_FENCED 1 \
  --setenv PATH "$P/.venv/bin:/usr/local/bin:/usr/bin:/bin" \
  --unsetenv SSH_AUTH_SOCK --unsetenv ANTHROPIC_API_KEY --unsetenv DBUS_SESSION_BUS_ADDRESS --unsetenv DISPLAY \
  -- "$@"
