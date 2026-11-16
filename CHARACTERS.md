# Characters

- Tosbi (main): calm, curious turtle with a surprise shell. pipeline/tosbi.py. Voice: Kokoro af_heart, EN speed 0.92,
  TR speed 0.9, pitch x1.16 (`asetrate=SR*1.16,aresample=44100,atempo=0.95`).
- Zıpzıp (recurring friend, introduced 2026-11-16, first episode: vehicles / ep05): quick, impatient little rabbit who
  always wants to go first, and learns to take turns, share and wait (themes: patience, sharing, taking turns).
  Drawing: pipeline/zipzip.py `zipzip(x, y, scale, expr=happy|talk|surprised, blink, ear, look, flip, squash)`, faces left
  toward Tosbi, stands on the front grass (layout key ZIP). Colors: fur #F6D7B8, paws #E8B98F, belly #FFF4E6,
  inner ears/cheeks #FF9AA2, teal scarf #2BB3A3 with yellow dots #FFE066, outline #3B2A20.
  Voice: Kokoro af_bella, EN speed 1.0, TR speed 0.98, pitch x1.30 (engine VOICES["zip"]). In episodes.py a line part
  spoken by him has a third element "zip"; a segment with friend=True brings him in (hop in, hello, "Let's take turns!").
  Next: at most one new recurring character per month (next earliest: December 2026).
