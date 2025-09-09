# Frogger (Docker)

Classic arcade-style Frogger built with Pygame (assets and layout per current README).

## Build

```bash
docker build -t frogger .
```

## Run (Linux, graphics + sound via PulseAudio)

### Allow X access (once per session)
```bash
xhost +local:docker
```

### Run the container
```bash
docker run --rm -it \
  --name frogger \
  --user $(id -u):$(id -g) \
  -e DISPLAY=$DISPLAY \
  -e SDL_VIDEODRIVER=x11 \
  -e XDG_RUNTIME_DIR=/run/user/$(id -u) \
  -e PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
  -e PULSE_COOKIE=/run/user/$(id -u)/pulse/cookie \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v /run/user/$(id -u)/pulse:/run/user/$(id -u)/pulse \
  frogger
```

## Native Run (Optional)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python FROGGER_RUN.py
```

## Notes

- If you see “X11 connection rejected”, run `xhost +local:docker` again.
- For ALSA instead of PulseAudio: add `--device /dev/snd -e SDL_AUDIODRIVER=alsa`.