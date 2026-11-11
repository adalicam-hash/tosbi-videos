# Tosbi & Friends — production format

Channel: Tosbi & Friends (@TosbiFriends). Ages 2–6. Made for Kids. Calm pacing.
Character: Tosbi, a calm, curious turtle; a surprise pops out of his shell every episode (see pipeline/tosbi.py, palette in sheet).

## Language model (decided 2026-11-11)
- ONE video per episode, primary audio ENGLISH, extra YouTube audio track TURKISH.
- On-screen text stays ENGLISH (key words: colors, numbers, "Bye-bye!") — it teaches English to Turkish kids too.
- EN voice: Kokoro `af_heart`, speed 0.9, pitched with ffmpeg `asetrate=SR*1.16,aresample=44100,atempo=0.95`.
- TR track: same voice. Turkish parts = espeak-ng "tr" phonemes (replace `ɫ`→`l`) fed to Kokoro with is_phonemes=True;
  English words inside TR lines are voiced natively in English (e.g. "Kırmızı bir top! Red!").
- TR track = full mix (voice + music + sfx), because a YouTube audio track replaces the whole audio.

## Timing rules
- Visual event first (ball pops etc.), then lines in BOTH languages start after it.
- On-screen English word appears when the English word is spoken (both tracks).
- Tosbi's mouth animates during the union of EN and TR speech windows.
- Leave short gaps after each new English word so the TR track can repeat it.

## Publishing
- Push the final EN video to this repo (shorts/ or long/), schedule it in Metricool (brand 8030099) as a DRAFT
  via raw.githubusercontent.com URL: type short/video, madeForKids=true, category EDUCATION, EN title, EN+TR description.
- Send the TR track mp3 to the owner; they add it in YouTube Studio → Subtitles/Languages → Turkish → Audio.
- Owner approves every draft in Metricool. Nothing auto-publishes without approval.

## Models (all free, fetched from GitHub releases / PyPI)
- kokoro-onnx: github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/{kokoro-v1.0.int8.onnx,voices-v1.0.bin}
- pip: kokoro-onnx soundfile cairosvg phonemizer espeakng-loader librosa
