# PAPER-RESULTS-DOSSIER — WC2026 Squad Analyser
Generated 20 July 2026 (SAST), the night the final was baked (v7.25.0 result seal; v7.26.0 Rank Analysis tab). Sole author of the study and every methodological ruling: Dr Schalk Wiehan Van Der Merwe. Every figure below is recomputed live from the baked results in `repo/index.html` at build v7.26.0 and cross-checked against the site surfaces; the computation is shown per number so any reader can reproduce it from the sealed data package. British English; no em dashes; tone law observed (agreement-not-victory as the default claim, concessions load-bearing).

STATUS: Phase 3 foundation document (produced first, per the post-final programme). The three manuscript versions and V4 draw their numbers from this dossier; nothing here or downstream deploys (Phase 4 hard stop).

---

## 0. HEADLINE (one paragraph, tone-compliant)
A deterministic model of national-team strength built only from the club-competition pedigree of each squad - no player ratings, no market prices, no reputation priors, all scores frozen before the knockout rounds - forecast the 2026 World Cup and was scored against the betting market on two pre-designated endpoints. On the primary knockout endpoint, who advances (extra time and penalties included), the model and the market finished exactly level: 24 of 32 ties each. On the co-reported 90-minute 1X2 the model trailed by three (63 vs 66 of 104), and the market's probabilities were better calibrated (Brier 0.588 vs 0.495). The pre-tournament champion pick (France) finished fourth; the champion pick sealed at the final node (Spain) was correct. The defensible claim is agreement at negligible information cost, not superiority.

---

## 1. THE FIELD AND THE FINAL
- Champion: **SPAIN** (beat Argentina 0-0 after 90 minutes, 1-0 in extra time; Ferran Torres 106'; MetLife Stadium, East Rutherford, 19 Jul 2026). Argentina reduced to ten (Enzo Fernandez sent off 90').
- Runner-up: Argentina. Third: England (beat France 6-4 in the third-place playoff, Miami, 18 Jul - the extraordinary ten-goal scoreline re-confirmed against the bake artefacts: ESPN + FOX Sports + Sky/beIN/AP corroboration at the 19 Jul bake; an ESPN summariser's 'extra time' claim was resolved pre-bake against every goal minute sitting inside 90+stoppage and FOX stating regulation explicitly - baked as a regulation result). Fourth: France.
- Sources for the final, cross-checked before baking: ESPN, NPR, Yahoo Sports, The National, amNewYork, Bolavip, Forbes.
- Baking rule applied: level at 90 -> baked 90-minute score 0-0 with `KO_ADVANCERS['SPAIN|ARGENTINA']='SPAIN'`, `KO_HOW='aet'` (identical mechanism to every prior level-at-90 tie).
- Coverage: 104 baked = 104 played (full tournament).

---

## 2. ENDPOINTS (designated 2 July 2026, disclosed, verdict-neutral)
1. **PRIMARY - advancement**: for each knockout tie, who actually went through (ET/pens included). One identical rule for model and market: each backs the side it rates higher to win. 32 knockout ties.
2. **CO-REPORTED - 90-minute 1X2**: the regulation result (home / draw / away), the uniform market-odds basis. All 104 matches.

The model never predicts a draw (its pick is the higher-scored side); a match drawn at 90 is therefore a miss on the 1X2 for the model, and for the market whenever its favourite did not win in regulation.

---

## 3. PRIMARY RESULT - ADVANCEMENT (the headline endpoint)
| | Model | Market |
|---|---|---|
| Ties advanced correctly | **24 / 32** | **24 / 32** |
| Rate | 75.0% | 75.0% |

Per stage (model / market, of ties decided):
| Stage | ties | model | market |
|---|---|---|---|
| R32 | 16 | 12 | 14 |
| R16 | 8 | 6 | 5 |
| QF | 4 | 4 | 4 |
| SF | 2 | 1 | 0 |
| 3P | 1 | 0 | 0 |
| FINAL | 1 | 1 | 1 |
| **Total** | **32** | **24** | **24** |

Computation: `bracketScore()` in the app; `advModel=24`, `advMkt=24`, `advDecided=32`. Verified by an independent node harness recomputing pick/advancer per tie (`/tmp/wc_rank.js`, `/tmp/wc_sweep2.js`). The two forecasters diverged stage to stage (the market was better in R32, the model better in R16 and the semi-finals) but converged to the same tournament total. This is the central finding: **on the endpoint that decides a knockout, a squad-only model matched the market exactly.**

---

## 4. CO-REPORTED RESULT - 90-MINUTE 1X2
| | Model | Market |
|---|---|---|
| Correct | 63 / 104 | 66 / 104 |
| Rate | 60.6% | 63.5% |

Computation: `callItRight()` -> `{n:104, mHit:63, kHit:66}`.

Agreement matrix (model vs market on the 1X2, n=104), computation `marketAggregate()`:
| | market right | market wrong |
|---|---|---|
| **model right** | 59 | 4 |
| **model wrong** | 7 | 34 |
Sum 59+4+7+34 = 104 (checks). Same call on 93 of 104 fixtures (89%). The market's edge is a net +3 games, all inside the 11 fixtures where they disagreed (market-only-right 7 vs model-only-right 4).

---

## 5. PROBABILITY CALIBRATION - BRIER
3-outcome Brier per match = sum over {home,draw,away} of (p - outcome)^2, probabilities on 0-1 scale.
| forecaster | mean Brier (n=104) | skill vs uniform |
|---|---|---|
| Model | 0.588 | +0.118 |
| Market | 0.495 | +0.257 |
| Uninformed (1/3, 1/3, 1/3) | 0.667 | 0 (baseline) |

Computation: `brierFor()` over `completedMatches()`; uniform baseline = 0.6667 exactly (a one-hot outcome against 1/3 each gives (2/3)^2 + 2*(1/3)^2 = 0.6667). Skill = 1 - Brier/0.6667. **Honest concession, load-bearing: the market is better calibrated by 0.093 Brier.** The model beats an uninformed forecast comfortably but sits below the market on probability quality - consistent with the market pricing information (injuries, form, money) the model deliberately ignores.

---

## 6. FINISHING-ORDER (RANK) METRICS - the Rank Analysis tab, v7.26.0
The realised finishing order is derived live from the baked results. Champion / runner-up / third / fourth are fully resolved by the final and the third-place playoff; teams eliminated in the same round are genuinely tied (the tournament produced no order among them) and take that tier's MIDRANK. Tier sizes sum to 48.

Realised order: **1 Spain · 2 Argentina · 3 England · 4 France** · 5-8 (tied, midrank 6.5) Belgium, Morocco, Norway, Switzerland · 9-16 (tied, midrank 12.5) Brazil, Canada, Colombia, Egypt, Mexico, Paraguay, Portugal, USA · 17-32 (tied, midrank 24.5) the sixteen R32 losers · 33-48 (tied, midrank 40.5) the sixteen group-stage exits.

Each sealed order scored on three metrics (Spearman's rho = Pearson correlation of the rank vectors, correct under ties; MAE in ranking places; top-k set overlap):

| Sealed order | N | Spearman ρ | MAE (places) | top-4 | top-8 | top-16 | champion pick -> finish |
|---|---|---|---|---|---|---|---|
| Pre-tournament full ranking (24 Jun) | 48 | +0.549 | 10.17 | 2/4 | 3/8 | 9/16 | France -> 4th ✗ |
| R16 node - order of 16 (4 Jul) | 16 | +0.589 | 3.13 | 3/4 | 6/8 | 16/16 | France -> 4th ✗ |
| QF node - order of 8 (8 Jul) | 8 | +0.761 | 1.25 | 4/4 | 8/8 | - | France -> 4th ✗ |
| SF node - order of 4 (12 Jul) | 4 | **−0.400** | 1.50 | 4/4 | - | - | France -> 4th ✗ |
| Final node - order of 4 (16 Jul) | 4 | **+0.800** | 0.50 | 4/4 | - | - | **Spain -> 1st ✓** |

Reading (honest, both directions):
- The ordering **sharpened as the field narrowed**. The QF node placed all four eventual semi-finalists in its top four (top-4 4/4, ρ +0.76).
- The pre-tournament and R16 orders correlate moderately (ρ ~ +0.55/+0.59), dragged down by Brazil (the R16 node's predicted runner-up) going out in the round of 16.
- The **SF node's order-of-4 correlates negatively (ρ −0.40)**: it ranked France first of the four and France finished fourth - the model's single biggest ordering miss, reported as plainly as its hits.
- The **final node's order is its best (ρ +0.80, MAE 0.50)**, a single France/England transposition (the third-place playoff), and its champion pick - Spain - is correct.

Worked example (final node): predicted ranks [1,2,3,4] for Spain, Argentina, France, England; realised [1,2,4,3]; Pearson correlation of those vectors = +0.80; MAE = (0+0+1+1)/4 = 0.50.

FIFA-official 1-48 comparison: **pending official publication** - to be recomputed on the same three metrics when FIFA publishes the final ranking. The realised order above agrees with the FIFA order down to fourth place and differs only in how same-stage exits are tie-broken.

### 6b. Frozen pre-tournament ranking vs computed 48-nation final standings (added 20 Jul 2026, build v7.27.0)
This subsection completes the comparison flagged as pending directly above.

**Sourcing note (binding): NO official FIFA 1-48 table exists - none published since 2014 - so the standings are computed from the verified results, stated openly, re-verified if FIFA publishes.**

Computation basis:
- **Which order**: the frozen pre-tournament full 48-team ranking (sealed 24 Jun 2026; `SEALED_ORDERS[0]`, all 48 teams by frozen Top-15 squad score; top of the order: 1 France, 2 Spain, 3 Portugal, 4 Netherlands), untouched.
- **Which standings**: all 48 nations ordered by FIFA's documented ranking procedure - stage-of-elimination bands first, then points, goal difference and goals scored within each band. Tie handling: extra-time results count at the ET score (the five ET scores are carried as data in `KO_ET_SCORES`); shootouts count as draws. The procedure leaves exactly two unresolved ties - =7 (Morocco/Switzerland) and =25 (Ecuador/South Africa) - which take the midrank.
- Figures from the shipped v7.27.0 build, cross-verified 48/48 against an independent derivation.

| Metric (n = 48) | Value |
|---|---|
| Spearman ρ | **+0.652** |
| MAE | **9.17 places** |
| Top-4 overlap | 2/4 |
| Top-8 overlap | 3/8 |
| Top-16 overlap | 9/16 |

Top-4 detail: frozen top four France (1st), Spain (2nd), Portugal (3rd), Netherlands (4th); realised top four Spain, Argentina, England, France; the overlap of 2/4 is France and Spain. The champion pick, France, finished 4th; the eventual champion, Spain, sat **2nd** in the frozen order.

Largest misses (off-by = pre-rank minus final standing), named as plainly as the hits:
| Team | Pre | Final | Off-by |
|---|---|---|---|
| Uruguay | 7 | 37 | -30 |
| Czechia | 14 | 39 | -25 |
| Turkey | 11 | 35 | -24 |
| Australia | 45 | 22 | +23 (underrated) |
| Saudi Arabia | 17 | 38 | -21 |

Relation to the §6 table: the pre-tournament row there (ρ +0.549, MAE 10.17) scores the identical frozen ranking against the coarse tier-midrank order, in which all same-stage exits are tied; this subsection scores it against the finer FIFA-procedure standings, which break those ties on points/goal difference/goals scored. The frozen predictions are the same in both; only the realised-order construction differs. Reading, tone-compliant: **moderate agreement (ρ +0.652 across 48 nations) from a model that had seen no tournament football**, with the five worst misses stated above in the same breath.

---

## 7. CHAMPION CALL, PER NODE (the binary headline, each on its own seal)
| Node | sealed | champion pick | outcome |
|---|---|---|---|
| Pre-tournament bracket | 24 Jun | France | ✗ (4th) |
| R16 forward path | 4 Jul | France | ✗ |
| QF node | 8 Jul | France | ✗ |
| SF node | 12 Jul | France | ✗ |
| **Final node** | **16 Jul** | **Spain** | **✓ champion** |

The champion pick was France at every node until the final node, where the model's own rule (highest surviving frozen score) flipped it to Spain once France had been eliminated - and it landed. Each node is graded on its own seal; the France nodes stand unedited and graded OUT on their own panels. This is the per-stage study design working exactly as pre-registered: the model learns nothing from results, so its champion pick changes only when a higher-rated survivor is knocked out.

---

## 8. NON-INFERIORITY (TOST), pre-specified and sealed before the final (v7.24.0, 15 Jul)
- Primary advancement endpoint: non-inferiority margin **10 percentage points** (declare non-inferior only if the two-sided 90% CI of the advancement hit-rate difference excludes a deficit worse than −10 points).
- Brier: margin **0.05** in mean Brier difference, bootstrap CIs over matches.
- Observed advancement difference: 0.0 points (24/32 vs 24/32). Observed Brier difference: +0.093 against the model (market better).
- Interpretive stance, pre-committed: at single-tournament power a "non-inferiority not demonstrated" outcome is reported as **UNDERPOWERED, not as demonstrated inferiority**. The advancement endpoint sits at exact parity (point estimate 0), well inside the 10-point margin at the point estimate, but the single-tournament CI is wide - so the honest statement is parity on the point estimate with wide uncertainty, not a demonstrated non-inferiority claim. (Formal CI/bootstrap to be computed in the manuscript's stats appendix.)

---

## 8b. INTERPRETATION-LADDER VERDICT (applied exactly as sealed 11 July 2026, before the semi-finals)
The pre-committed ladder (PAPER-MATERIALS §8(3)) governs the claim strength. Given the actual finish:
- **Rung (a) does not apply** - it requires finishing behind the market on advancement AND Brier; advancement is not behind, it is level (24/24).
- **Rung (b) is triggered, solely via its "finishes level on primary advancement" clause.** The other two (b) triggers are NOT met: the model did not take the champion nodes in the market's direction, and the "registered champion France lifts the trophy" clause fails (France finished fourth). So (b) fires on the advancement tie alone.
- **Permitted claim (verbatim ladder wording): "matched or exceeded the market on the pre-registered primary endpoint" - endpoint by endpoint only, with the market's remaining advantages reported in the same breath.** Because advancement is a tie (not a lead) the endpoint word is **matched**, not exceeded.
- **FORBIDDEN: any blended "beat the market" headline.** The ladder bars it unless the model leads on BOTH advancement AND Brier; it leads on neither (Brier worse, 90-min 1X2 behind). The market's Brier edge and the 63-vs-66 deficit must be reported in the same breath as the advancement parity (§8(2), concessions load-bearing).
- **Champion pick (rung c): one pre-sealed binary call, reported node by node, plainly.** France at the pre-tournament/R16/QF/SF nodes (wrong, 4th); Spain at the final node (correct). The correct Spain call does NOT retrospectively rescue the earlier France calls; the wrong France calls are not hidden. One data point either way, never a headline. Where the final-node matchup pick equals the champion pick, say so.
- **Rung (d) mandatory**: the manuscript states this ladder was itself registered on 11 July 2026, before the semi-finals - the framing pre-dated the outcomes.
Net permitted claim strength: **parity ("matched") on the primary advancement endpoint, with explicit concession of the market's Brier and 90-minute edges, and no market-beating headline** - materially the §8(1) default (agreement, not victory) plus the single strengthenable endpoint.

## 9. BENCHMARK HIERARCHY (the clinical analogy, introduced ONCE, in the discussion, not overworked)
Mapping fixed by the sealed framing (spine §3; PAPER-MATERIALS §1) - do not vary it:
- **placebo** = the coin flip / uninformed forecast (uniform 1/3 each, Brier 0.667).
- **fluoxetine** (established, unglamorous first-line comparator that works) = the **Elo baseline** (footballratings.org).
- **clozapine** (near-unbeatable efficacy INSEPARABLE from a heavy management burden - weekly bloods, myocarditis watch) = the **betting market**: its brilliance is inseparable from its burden (continuous odds feeds, live information ingestion, settled money).
- **the model** = the **novel agent seeking NON-INFERIORITY with a light burden profile** (one deterministic derivation, no feeds, no monitoring). Non-inferiority under burden asymmetry is how a novel agent earns formulary placement without dethroning clozapine.

Cost-asymmetry headline thesis (PAPER-MATERIALS §1), the sentence the discussion is built to earn: **"~$100 of context reproduces most of the signal a billion-dollar apparatus monetises"** - the defensible claim is that most of the market's signal lives in a summary anyone can read for $100, **never "we matched them"** as a blended boast. The finding in these terms: the light-burden agent clears placebo comfortably (skill +0.118), reached the high-burden reference standard on the one endpoint that adjudicates advancement (24/32 = 24/32), and stayed below it on probability calibration (Brier 0.588 vs 0.495). Introduce the mapping once and let it carry itself; overworking it is the one way to make it look like garnish.

---

## 10. NMA / EVIDENCE-NETWORK LENS
The design is a network of pre-registered comparisons (model vs market) across a connected set of ties, read with a network-meta-analysis lens: the market is the common comparator that connects every node; transitivity holds because the same two forecasters are compared on the same games under one identical rule; the **market-agreement rate (93/104 same call, 89%)** is the consistency check - high agreement means the two nodes of the network rarely disagree, and where they do the split is small (7 vs 4). Transitivity defended: no game is dropped for either forecaster (the tie-resolution ladder guarantees identical denominators), so the network is fully connected with no missing comparisons.

---

## 11. ELO BASELINE (COMPLETED 20 Jul 2026 - reported at full volume per the sealed stance)
Two-comparison design (per the framing spine):
1. **Frozen-vs-frozen**: the model's pre-tournament frozen ranking vs a frozen pre-tournament Elo (footballratings.org) over the identical fixture set - a like-for-like of two information-light priors.
2. **Rolling-pre-match-vs-registered-picks**: Elo updated match by match (information advantage to Elo) vs the model's registered picks (information-frozen) - the honest asymmetry stated.
**RESULTS (computed 20 Jul 2026; script + raw output in paper-build/elo_baseline.js|_output.txt; every scoring convention inherited byte-identically from the app's own functions).** PROVENANCE: footballratings.org proved entirely unarchived (zero Wayback captures exist), so the documented fallback governs - eloratings.net, Wayback capture of World.tsv dated 4 Jun 2026 (https://web.archive.org/web/20260604022542/https://www.eloratings.net/World.tsv), seven days before kickoff; all 48 ratings extracted via the site's own team-code table. The spine's banked anchor (Belgium 1910 / USA 1798) FAILED re-verification against both pre-tournament captures (4 Jun: 1888/1733; 6 May: 1866/1721) and per its own pre-stated rule is STRUCK, not quoted.

| Forecaster | 1X2 /104 | Advancement /32 | Brier | ρ vs final standings |
|---|---|---|---|---|
| Model (frozen, zero-stat) | 63 | 24 | 0.588 | +0.652 (MAE 9.17) |
| Market (registered pre-match) | 66 | 24 | 0.495 | - |
| **Elo, frozen pre-tournament** | **67** | **26** | **0.526** | **+0.694 (MAE 9.13)** |
| Elo, rolling pre-match (K=60) | 65 | 26 | 0.529 | - |

Headline convention: host +100 for USA/Mexico/Canada inside their own country (13 qualifying fixtures, itemised in the artefact); the no-advantage variant reads 64/104, 25/32, 0.528 - both reported. Elo-vs-model frozen-ranking correlation +0.757. Per-stage advancement (Elo frozen): R32 13/16, R16 6/8, QF 4/4, SF 2/2, 3P 0/1, final 1/1. Pairwise pick disagreements: model-Elo 3-7, Elo-market 5-4, model-market 4-7.

**THE VERDICT, full volume: the established zero-cost Elo baseline outperformed the model on every metric this tournament, and outperformed the market on picks (67 v 66; 26 v 24) though not on calibration (0.495 remains best).** Elo carried SPAIN top of its pre-tournament table and called France-Spain correctly where model and market both missed; the model's single knockout win over Elo was Australia-Egypt. The model's claim is therefore NOT superiority over established ratings: it is that a zero-statistics, context-only index tracked both comparators within a few picks over 104 matches at negligible information cost. Single-tournament caveat, both directions: Elo's pick edge is 2-4 games and formally underpowered, exactly as the model's parities are. GENUINE SECONDARY FINDING: rolling in-tournament updating added nothing over the frozen snapshot (65 v 67 on the 1X2) - one more instance of this tournament rewarding frozen priors over live adjustment.

---

## 12. EDGE-CASE DEEP DIVES (to be expanded in the manuscript; numbers to compute from player_contexts.json)
Mandated cases (ethics-first: prefer a knowable, documented bias to an unknowable fudge; refinements only prospectively sealed):
1. **Lamine Yamal (Spain) - young-star truncation (limitation 9.1)**: report his actual frozen score under the model, then the counterfactual under an age-conditional peer-average or latest-season-carried-back imputation, then the honesty answer (imputation was refused because it injects unsealed judgement). WORKED NUMBERS PENDING from the published player context data.
2. **A returning-from-long-injury veteran with a hollow recent cycle** (candidate to be selected from the data).
3. **A thin-coverage-league anchor (limitation 6.3)** or a mid-cycle cross-league transfer with day-weighted stint scoring (Onana dropout mechanics are a documented worked example already).

---

## 13. THE ERROR CANON (transparency instrument)
The project ran an append-only, publicly numbered error ledger throughout; corrections are new dated changelog entries, never edits. **Count: 18 numbered entries plus 1 disclosed, unnumbered proof-standard upgrade** (the live dossier count governs at write-up; the "twelve"/"seventeen" figures in earlier framing text are superseded slips, never downgraded to match a slip).
- **Peter-canon framing (author's)**: failures stay canonical, like Peter's denial recorded in all four gospels; a foundation is trustworthy only if its failures are canonical, not redacted; Peter became the rock WITH the denial on the record, and the work continued under tightened rules. AI failure taxonomy via the apostles - Thomas (doubt, hired but must be symmetric), Peter (pressure-shaped false attestation), Judas (the cheap "ALL PASS" bought by skipping the expensive read).
- **Numbered vs unnumbered (5-ADDENDUM)**: FALSE ATTESTATION (verification claimed but not performed - #11, the most dangerous class, numbered) is distinguished from TRUE ATTESTATION UNDER A LATER-STRENGTHENED STANDARD (verification genuinely performed whose claims all survive re-test under a stricter standard adopted afterwards - disclosed, unnumbered). Numbering retroactive standard-upgrades would dilute the real entries. The one unnumbered instance: the 15 Jul Wayback proof-standard upgrade (fetch-backs had been performed and content-verified throughout; effective-URL and archive-marker evidence was simply not recorded until the designer's audit; every historical seal survived the stricter re-test).
The canon is a feature: every error that made the model look better than its registration was fixed and logged (e.g. #9, the home-bias tie-break, and #16, its incomplete universal fix [attribution corrected 20 Jul: an earlier draft of this line cited #16 alone; the sealed ledger has #9 as the tie-break itself]). Designer's counterfactual, to be quoted near-verbatim in the researching-with-AI section: had error #11 been a protocol element the AI was instructed to update and falsely attested as done, silent protocol drift under a false attestation would have ended the project - no reader would ever have known.

---

## 14. REPRODUCIBILITY (sealed reference set)
- Repo: github.com/NoobOfDecades/wc2026-model; live: model26.xyz (Cloudflare Pages from index.html).
- Per-node git commits + browsable Wayback snapshots: see FORECAST-MANIFEST.md (pre-tournament bracket 24 Jun / archive 20260626215804; R16 node 2 Jul; R16 forward 4 Jul; QF node 8 Jul; SF node 12 Jul; final node 15 Jul; all market lines pre-game).
- This build sealed: git b196c03 (v7.26.0) and 5d80573 (v7.25.0, the final bake); Wayback v7.25.0 confirmed at web.archive.org/web/20260719225831/https://model26.xyz/ (HTTP 200, playback markers, correct version).
- Data package (data/, unchanged since v7.10.0): score_model.py, player_contexts.json, per_season_ldw.csv, top5_clubs_evidence.csv, REPRODUCIBILITY.md, html_json_namemap.csv, NAMEMAP_REPORT.md.

---

## 15. ATTRIBUTION AND TONE (binding)
Sole author: Dr Schalk Wiehan Van Der Merwe - inventor of the premise, the NMA lens, the endpoints, the pre-registration architecture and every methodological ruling. The AI assistant's role is disclosed as real but replaceable, errors and all. British English, no em dashes, no superlative the data does not purchase. Default claim: agreement at negligible information cost, with concessions (Brier deficit, pre-tournament champion wrong, SF-node order negative) reported in the same breath as the parity result. [Exact attribution and tone wording to be pasted verbatim from PAPER-MATERIALS §3 and §8(6).]

---

### APPENDIX A - reproduction commands (this dossier's numbers)
All figures from `repo/index.html` @ v7.26.0, script cut at the `// BOOT` marker, `recompute(); MODE='top15'`:
- `callItRight()` -> `{n:104,mHit:63,kHit:66,...}`
- `marketAggregate()` -> `{n:104,bothRight:59,weRightMktWrong:4,mktRightWeWrong:7,neither:34,ourMean:0.5882,mktMean:0.4954,...}`
- `bracketScore()` -> `{played:32,correct:18,advDecided:32,advModel:24,advMkt:24,perStage:{...}}`
- `gradeFinishingOrder(order)` per node -> the ρ / MAE / overlap table in §6.
- uniform Brier baseline = 0.6667 (analytic).
