# Xusniddin Tech render tools

- `reel.py spec.json out.mp4` — 1080x1920 motion Reel (kinetic text, blue gradient, generated background music).
  Scene types: `words`, `cards`, `number`, `cta`, `subscribe` (avatar + handle + "Obuna" -> "Yashang!" ending, always last).
- `carousel.py spec.json outdir` — 1080x1350 carousel pages (`cover`, `number`, `cards`, `cta`).
- `avatar.jpg` — profile photo used by the `subscribe` ending.
- `example_spec.json` — a full Reel spec.
Needs: python3, numpy, Pillow, ffmpeg, Inter Display fonts (/usr/share/fonts/opentype/inter/).
