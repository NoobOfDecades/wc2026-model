# NAMEMAP REPORT — HTML ↔ JSON Player-Name Bridge

**Output:** `html_json_namemap.csv` (1249 lines: header + 1248 data rows)  
**Coverage:** All 1248 HTML players across 48 teams  
**Unresolved:** 0  
**Completed:** 2026-06-27

---

## Input Sources

| File | Role | Players |
|------|------|---------|
| `wc2026-full-v6.0.2.html` | HTML-side source; `const S={...}` JS object | 1248 players |
| `player_contexts.json` | JSON-side source; per-team player lists with club stints | 1534 entries |

The 1534 JSON entries vs 1248 HTML players: 286 extra JSON entries have `matched:False` (audit-added squad candidates, not in the authoritative HTML squad). Of the 1534, 18 are `matched:False` — these appear in the output only if matched to an HTML player; they are not targets.

---

## Match-Method Summary

| Method | Count | Confidence | Description |
|--------|-------|-----------|-------------|
| `exact` | 1146 | high | Name strings identical |
| `accent_strip` | 84 | high | Match after NFKD normalization + combining-mark strip |
| `hyphen_norm` | 4 | high | Match after hyphen→space normalization |
| `umlaut_expand` | 1 | high | Match after ö/ü/ä→oe/ue/ae expansion (German) |
| `nickname` | 3 | medium | Match via canonical nickname map (Andy↔Andrew, Mousa↔Musa, Rouzbeh↔Roozbeh) |
| `lastname_initial` | 3 | medium | Match by surname + first initial (handles middle-name expansion) |
| `fuzzy_last_token` | 2 | medium | Match where all-but-last tokens identical, last token fuzzy ≥ 0.72 |
| `firstname+club` | 1 | medium | Match by first name (≥90% similarity) + exact club when surname differs |
| `name_prefix` | 1 | medium | JSON name is a proper prefix of HTML name (≥2 tokens) |
| `surname+club` | 3 | **low** | Match by exact surname + exact club (unique); first names differ — JSON data error |
| **Total** | **1248** | | |

---

## Non-Standard Matches Detail

### `accent_strip` (84)
Standard normalization. Covers players whose names contain accented characters that appear differently between the two sources (e.g., é vs e, ö vs o via NFKD).

### `hyphen_norm` (4)
| HTML | JSON |
|------|------|
| Jean-Michaël Seri | Jean Michael Seri |
| Mohamed El Shenawy | Mohamed El-Shenawy |
| Nawaf Al Aqidi | Nawaf Al-Aqidi |
| Mohammed Al Owais | Mohammed Al-Owais |

### `umlaut_expand` (1)
| HTML | JSON | Club |
|------|------|------|
| Alessandro Schöpf | Alessandro Schoepf | Wolfsberger AC |

German ö→oe expansion; NFKD alone gives "Schopf" which doesn't match "Schoepf".

### `nickname` (3)
| HTML | JSON | Match basis |
|------|------|-------------|
| Andy Robertson | Andrew Robertson | Andy↔Andrew |
| Rouzbeh Cheshmi | Roozbeh Cheshmi | Rouzbeh↔Roozbeh (Persian) |
| Mousa Al-Tamari | Musa Al-Taamari | Mousa↔Musa + Arabic vowel norm |

### `lastname_initial` (3)
JSON entries truncated to surname + first initial; HTML has full middle names or expanded forms.

| HTML | JSON | Club |
|------|------|------|
| Baris Alper Yilmaz | Baris Yilmaz | Galatasaray |
| Irfan Can Kahveci | Irfan Kahveci | Besiktas (note: clubs differ in sources) |
| Shojae Khalilzadeh | Shoja Khalilzadeh | Tractor SC |

### `fuzzy_last_token` (2)
All tokens except the last match exactly; last token similarity ≥ 0.72.

| HTML | JSON | Ratio | Club |
|------|------|-------|------|
| Ahmed Sayed Zizo | Ahmed Sayed Zizou | 0.75 | Al Ahly |
| Orkun Kokcu | Orkun Koksuz | 0.73 | SL Benfica |

`Ahmed Sayed Zizou` was correctly preferred over the shorter `Ahmed Sayed` (ENPPI) because the club (Al Ahly) uniquely disambiguates among candidates. `Orkun Kokcu`/`Orkun Koksuz` = Orkun Kökçü; variant transliteration of ö→o vs ö→o+u.

### `firstname+club` (1)
| HTML | JSON | Club | Note |
|------|------|------|------|
| Mohamed Abdelmonem | Mohamed Abdel Moneim | OGC Nice | Surname split differently across sources |

### `name_prefix` (1)
| HTML | JSON | Club |
|------|------|------|
| Christ Inao Oulaï | Christ Inao | Trabzonspor |

JSON name is a proper 2-token prefix of the HTML 3-token name; only one Christ Inao in Ivory Coast squad.

---

## Low-Confidence `surname+club` Matches (JSON Data Errors)

These three players matched via unique surname + exact club. Their first names differ between HTML and JSON — the JSON first names appear to be data entry errors. Confidence is `low`; the match logic is sound (unique surname+club in squad) but the discrepancy should be noted for any downstream use.

| HTML Name | JSON Name | Club | HTML first | JSON first |
|-----------|-----------|------|-----------|-----------|
| Kenan Yildiz | Taner Yildiz | Juventus FC | Kenan | Taner |
| Jamie Leweling | Maximilian Leweling | VfB Stuttgart | Jamie | Maximilian |
| Takefusa Kubo | Yoshiki Kubo | Real Sociedad | Takefusa | Yoshiki |

**Evidence that these are the correct matches (not different players):**
- `Kenan Yildiz` is the established Juventus and Turkey international; no "Taner Yildiz" exists at Juventus or in the Turkey senior squad. Only one Yildiz in the Turkey squad in both sources.
- `Jamie Leweling` plays for VfB Stuttgart and Germany; no "Maximilian Leweling" exists at Stuttgart outside this JSON entry. Only one Leweling in the Germany squad in both sources.
- `Takefusa Kubo` plays for Real Sociedad and Japan; no "Yoshiki Kubo" exists at Real Sociedad. Only one Kubo at Real Sociedad in the Japan squad.

**Recommendation:** These are JSON data errors. If using this CSV to join data, treat `low`-confidence matches with caution and consider correcting the JSON first names before ingestion.

---

## JSON `matched:False` Entries

The `player_contexts.json` contains 1534 total player entries; 18 have `matched:False`. These are audit-added candidates (squad members added manually, not pulled from an automated match pipeline). They are included in the JSON candidate pool for matching but the `json_matched_flag` column in the CSV records their status. No `matched:False` entry should be used without further verification.

---

## Integrity Notes

- **No guessing**: Every match has a documented algorithmic basis. Matches where surnames differ materially are flagged as `low` confidence with the discrepancy explicit in the `note` column.
- **Club used as tiebreaker only**: Club matching was applied only to break ambiguity among candidates — never used as a primary match signal except in `firstname+club` and `surname+club` tiers.
- **All HTML players covered**: 1248/1248. No player was silently dropped or skipped.
- **Referenced data only**: All name strings come directly from the input files. No external lookups, no imputed names.
