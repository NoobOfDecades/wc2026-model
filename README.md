# WC2026 Squad Strength Model — model26.xyz

**Live site: https://model26.xyz/**

A frozen, pre-registered squad-strength model forecasting the 2026 FIFA World Cup - built from club context only (zero per-player performance statistics), sealed before kickoff, and scored openly against the betting market.

## What makes it different
- **Pre-registration, provable:** six forecast nodes (pre-knockout bracket, R32, R16, R16 forward path, QF, SF, final) each frozen in a dated git commit and independently witnessed by an Internet Archive capture *before* the games they predict. The site's Model tab carries **The Sealed Record** - one browsable snapshot URL per registration.
- **The model never learns from results.** One frozen ranking, read out at every stage against whoever actually survived.
- **Honest scoreboard:** every prediction graded on the site, hits and misses alike, against pre-game market odds captured in advance (never after kickoff, never swapped).
- **A published error ledger:** every mistake made in building and running the model - currently nineteen numbered entries - is documented in the site changelog rather than hidden. The correction record is the credential.

## Reproducibility
The `data/` directory contains the standalone scoring script, the raw per-player context inputs, per-season league strengths with sources, and `REPRODUCIBILITY.md`. Reimplementation is invited.

## Provenance
This repository's commit log is the primary timestamp trail; the Internet Archive captures listed on the site are the independent witness. The written findings will be hosted on the site after the tournament concludes.
