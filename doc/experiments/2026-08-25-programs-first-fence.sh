#!/bin/sh
# The programs-first trial's fence (doc/experiments/2026-08-25-both.md).
# Not a tool: a record.  A node — gestate's andon — with exactly the three
# nouns doc/mediation-order.md wrote for it: its bundle, read-only; audio
# out; its own state directory, read-write.  Nothing else: no other tree,
# no network, an empty home.  AUDIO=alsa gives /dev/snd alone (the first
# attempt); AUDIO=pipewire adds the PipeWire socket (what it complained
# for).  NODE_STATE is the node's own directory.
G=/home/cheery/gestate
RT=/run/user/$(id -u)
STATE=${NODE_STATE:?the node state directory}
case ${AUDIO:-alsa} in
    alsa)     sock="" ;;
    pipewire) sock="--dir $RT --bind $RT/pipewire-0 $RT/pipewire-0" ;;
esac
exec bwrap --unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-net --die-with-parent --new-session \
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin \
  --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --tmpfs "$HOME" \
  --ro-bind "$G" "$G" --chdir "$G" \
  --dev-bind /dev/snd /dev/snd \
  --bind "$STATE" "$STATE" \
  $sock \
  --setenv HOME "$HOME" --setenv XDG_RUNTIME_DIR "$RT" --setenv NODE_STATE "$STATE" \
  --setenv PATH "$G/.venv/bin:/usr/bin:/bin" \
  --unsetenv SSH_AUTH_SOCK --unsetenv ANTHROPIC_API_KEY --unsetenv DBUS_SESSION_BUS_ADDRESS --unsetenv DISPLAY \
  -- "$@"
