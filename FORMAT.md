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

## Engine
- `python3 pipeline/engine.py OUT v|h seg1,seg2 [--long]` builds video + EN/TR mixes from pipeline/episodes.py.
- v = vertical Short (one segment, no repetition). h = 16:9 long video (several segments, --long adds 'say it with me' + 'where is the ...?' quiz).
- New content = add a segment to episodes.py (3 items) and, if needed, a drawing to items.py (original designs only).
- TR tracks are stored in tr_tracks/ for the owner to upload in YouTube Studio.

## Models (all free, fetched from GitHub releases / PyPI)
- kokoro-onnx: github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/{kokoro-v1.0.int8.onnx,voices-v1.0.bin}
- pip: kokoro-onnx soundfile cairosvg phonemizer espeakng-loader librosa

## Growth & evolution (owner request 2026-11-11)
The owner wants the channel to grow with new characters and new kinds of stories, steered by what viewers watch.
- Every weekly run starts with a performance review: Metricool YouTube analytics (getAnalyticsAvailableMetrics /
  getAnalyticsDataByMetrics, brand 8030099) for the last 28 days — views, watch time / average view duration,
  subscribers per video. Compare Shorts vs long, topic vs topic, EN vs TR interest (comments are off for Made for Kids).
- Record findings in PERFORMANCE.md (date, what was measured, what it suggests, what you changed). Keep it short.
- Decide the week's plan from the data: double down on topics/formats that keep viewers, drop what doesn't.
  With little data (first weeks), keep the proven format and change one thing at a time so effects are measurable.
- New characters: original designs only (never resemble existing franchise characters). Introduce at most one new
  recurring character per month, give it a clear, simple personality, add it to CHARACTERS.md with its drawing function,
  colors and voice settings, and keep Tosbi as the main character so the brand stays recognizable.
  First planned friend: Zıpzıp, a quick, impatient little rabbit (themes: patience, sharing, taking turns).
- New story formats are welcome (mini adventures, songs with original lyrics, "Tosbi & friend" dialogues, bedtime calm
  episodes), extending pipeline/engine.py as needed. Keep: ages 2–6, calm pacing, no scary or unsafe behavior,
  English key words on screen, both EN and TR tracks, event-first timing.
- Any big change (new character, new format) is announced in the weekly summary, and still goes out as a draft only.
