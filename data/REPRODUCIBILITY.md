# WC2026 Squad-Strength Model — Reproducibility & Verification

**Live model:** https://model26.xyz
**This package lets anyone independently reproduce the model's scores and audit its central claim.**

---

## The claim being made

> This model was built **without fitting**. Every weight comes from an **external, dated source**
> or a **stated mechanism**, chosen **before** seeing how it scores against the 2026 World Cup.
> There are **no free parameters tuned to make predictions look good**. Every dead end explored
> during development is documented in the model's "Model" tab, including the ones that were rejected
> *because* tuning them would have been fitting.

This is unusual. Most predictive models are optimised against the outcomes they are judged on.
This one deliberately is not — and this package exists so you don't have to take that on faith.

---

## What's in this package

| File | What it is |
|------|------------|
| `score_model.py` | A standalone, dependency-free Python script that computes every player's score from the raw inputs. Fully commented with the exact formula and the provenance of every constant. |
| `player_contexts.json` | The raw input: each player's club-by-club history ("stints") — which league, which season, days at the club, league finishing position, league size, and share of time in each competition. These are **public, verifiable facts about where players played** — NOT performance statistics. |
| `per_season_ldw.csv` | League strength per league **per season**: the average Opta Power Ranking of each league's top-5 clubs, as the league stood at that season-end. **Every row cites the exact Wayback Machine archive URL and date** it was extracted from. |
| `top5_clubs_evidence.csv` | The club-level evidence behind `per_season_ldw.csv`: for sampled leagues/seasons, the actual five top clubs and their individual ratings, so the league averages can be checked club-by-club. |

---

## How to reproduce the scores

```
python3 score_model.py
```

(Requires only Python 3 standard library. Place the three data files in the same directory.)

This writes `player_scores_reproduced.csv` and prints the team ranking. The per-player scores and
their ordering will match what the live model uses.

---

## How to audit the "no fitting" claim

The claim is not "the model is accurate" — it may or may not predict the knockouts well, and that
is part of the experiment. The claim is that **the inputs were not reverse-engineered from results.**
You can check this directly:

1. **Every league weight is externally sourced and dated.** Open `per_season_ldw.csv`. Each row has
   a `source_url` pointing to a specific Wayback Machine snapshot of the Opta Power Rankings, with an
   `as_of_date`. These snapshots **predate the 2026 World Cup**. The weights could not have been chosen
   to fit 2026 results because they were published before those results existed. Follow any URL and
   re-derive the top-5 average yourself.

2. **The normalisation and recency rules are stated mechanisms, not tuned values.** League weights are
   normalised to "Premier League of the same season = 1.000"; recency weights decline with age on a
   fixed schedule. These are design choices fixed in advance, documented in `score_model.py`, not
   numbers selected by trying many and keeping whichever scored best.

3. **The single scale constant affects nothing.** `SCALE = 0.00805852` multiplies all scores equally,
   so it changes no comparison and no prediction — only the printed magnitude.

4. **There are no per-team, per-player, or per-result adjustments anywhere.** Read `score_model.py`
   end to end: the same formula runs for every player. There is no special-casing.

5. **The rejected alternatives are documented.** The live model's "Model" tab records every lever that
   was tested and *rejected because adopting it would have been fitting* — e.g. steeper league-weight
   curves, finish-curve convexity, interaction terms — each rejected on principle (it improved
   agreement with results in a way that signalled overfitting), with the reasoning shown. A model that
   hides its dead ends cannot make this claim; this one shows them.

---

## The only true out-of-sample test

The model's predictions were registered before the knockout stage. The group stage is *in-sample* in
the weak sense that the squads were assembled before it, but the knockouts (Round of 32 onward) are the
genuine out-of-sample test: outcomes the model had no access to when its parameters were fixed. Judge
it there. An honestly-built model that predicts the knockouts poorly is a *useful* result — it would
show the limits of rating squads by competitive context alone. A fitted model that looked accurate
would teach nothing. This package exists so the difference can be verified rather than asserted.

---

*Generated for v7.0.0. A public version-control repository with timestamped commit history
(establishing the pre-registration dates) will be linked here once available.*
