#!/usr/bin/env python3
"""
WC2026 Squad-Strength Model — Reference Scoring Script (v7.0.0)
================================================================
This script REPRODUCES every player's squad-strength score from the raw, sourced inputs.
Its purpose is to make the model's central claim auditable by anyone:

    "This model was built WITHOUT FITTING. Every weight comes from an external, dated source,
     chosen before seeing how it scores against match outcomes. There are no free parameters
     tuned to make predictions look good."

If you run this script on the two provided data files, you will obtain the same player scores
the live model (model26.xyz) uses. You can then verify that NONE of the inputs were reverse-
engineered from the 2026 World Cup results — they are all prior, published facts.

------------------------------------------------------------------------------------------------
INPUTS (provided alongside this script):
  player_contexts.json   Each player's club-by-club history ("stints"), one record per player.
                         Per stint: league, season, days at club, league finishing position,
                         league size, and share of time in each competition (domestic / continental).
                         These are PUBLIC, VERIFIABLE FACTS about where players played — not stats.
  per_season_ldw.csv     League strength per league PER SEASON: the average Opta Power Ranking of
                         each league's top-5 clubs, as the league actually stood at that season-end.
                         Extracted from Opta Power Rankings bundles archived by the Wayback Machine.
                         Every row cites its exact archive URL and date. (LDW = League-Difficulty Weight.)

WHAT THE MODEL DELIBERATELY DOES NOT USE: individual player statistics (goals, assists, xG, minutes,
ratings), transfer/market values, bookmaker odds, or player reputation. The model rates a national
squad PURELY by the competitive context its players earned — which leagues, how strong those leagues
were that season, how their clubs finished, and how long they were there. Two famous players can score
very differently if their recent club context differs; an unknown player at a strong, high-finishing
club scores highly. This is the "Pure Vision".

------------------------------------------------------------------------------------------------
THE FORMULA (identical for every player; the ONLY season-varying input is the league weight):

  player_score = SCALE * SUM over stints [
                   duration_days
                   * recency(season)
                   * SUM over competitions in that stint [
                       time_share(competition)
                       * strength(competition, season)
                       * finish_quality
                     ]
                 ]

  where:
   recency(season):   2022-23 = 0.70, 2023-24 = 0.85, 2024-25 = 1.00, 2025-26 = 1.00
                      (older seasons count less; the current cycle counts fully)
   strength(domestic league, season):
                      = that league's top-5 Opta average THAT SEASON, normalised so the
                        Premier League of the SAME season = 1.000. (Per-season normalisation
                        removes year-on-year drift in the absolute Opta scale and expresses every
                        league as a fraction of the strongest league that season.)
                        Leagues with no per-season Opta data (minor/lower divisions) keep a single
                        static weight for all seasons — the least-assumption choice where no
                        season-resolved source exists.
   strength(continental competition):
                      UCL 1.15, UEL 0.90, UECL 0.70, LIBERTADORES 0.85, SUDAMERICANA 0.62,
                      AFC_CL 0.55, CONCACAF_CL 0.55, CAF_CL 0.52   (continental prestige weights)
   finish_quality:
                      domestic: (league_size - finishing_position + 1) / league_size   [linear]
                      continental: by stage reached — WIN 1.0, FINAL 0.9, SF 0.78, QF 0.66,
                        R16 0.54, KO_PLAYOFF 0.42, GROUP/LEAGUE_PHASE 0.30, QUALIFYING 0.15
   SCALE:             0.00805852  (a single global display constant; it scales all scores equally
                      and therefore affects NO comparison or prediction — only the printed number.)

Every one of these constants is a STATED MECHANISM or an EXTERNAL SOURCE, fixed before scoring.
None was selected to improve agreement with 2026 results. That is what "no fitting" means here.
------------------------------------------------------------------------------------------------
USAGE:
   python3 score_model.py
Outputs player_scores_reproduced.csv (team, player, score) and prints a team ranking.
"""
import json, csv
from collections import defaultdict

RECENCY = {'2022-23':0.70, '2023-24':0.85, '2024-25':1.00, '2025-26':1.00}
CONTINENTAL = {'UCL':1.15,'UEL':0.90,'UECL':0.70,'LIBERTADORES':0.85,'SUDAMERICANA':0.62,
               'AFC_CL':0.55,'CONCACAF_CL':0.55,'CAF_CL':0.52}
PROGRESS = {'WIN':1.0,'FINAL':0.9,'SF':0.78,'QF':0.66,'R16':0.54,'KO_PLAYOFF':0.42,
            'LEAGUE_PHASE':0.30,'GROUP':0.30,'QUALIFYING':0.15}
SCALE = 0.00805852
SEASONS = ['2022-23','2023-24','2024-25']

# Static fallback weights for leagues without per-season Opta data (minor/lower divisions).
# These are the model's single-snapshot weights; used for ALL seasons of such leagues.
STATIC_LDW = {
 'BUNDESLIGA_2':0.475,'SERIE_B':0.503,'LIGUE_2':0.399,'PORTUGUESE2':0.383,'AUSTRALIAN':0.383,
 'CYPRIOT':0.368,'ALGERIAN':0.337,'UZBEK':0.337,'IRISH':0.322,'BOSNIAN':0.322,'TUNISIAN':0.337,
 'JORDAN_L':0.291,'IVOREAN':0.307,'ARMENIAN':0.261,'GHANA_PL':0.276,'NZ_LEAGUE':0.184,
 'PANAMANIAN':0.215,'HAITIAN':0.153,'CURACAO_L':0.123,'PARAGUAYAN':0.368,
}

def load_per_season_ldw(path):
    raw = {}
    with open(path, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            try: raw[(r['league_key'], r['season'])] = float(r['top5_avg'])
            except (ValueError, KeyError): pass
    epl = {s: raw[('EPL', s)] for s in SEASONS}
    ldw = defaultdict(dict)
    for (lk, s), v in raw.items():
        if s in epl:
            ldw[lk][s] = v / epl[s]                       # normalise to EPL-of-that-season = 1.000
    for lk in ldw:
        if '2024-25' in ldw[lk]:
            ldw[lk]['2025-26'] = ldw[lk]['2024-25']       # carry latest verified season forward
    return ldw

def league_weight(ldw, league_key, season):
    if league_key in ldw and season in ldw[league_key]:
        return ldw[league_key][season]
    # Korean league is stored as a name-string in some records:
    if league_key and str(league_key).strip().lower().startswith('k') and 'league' in str(league_key).lower():
        if 'KOREAN' in ldw:
            return ldw['KOREAN'].get(season, ldw['KOREAN'].get('2024-25', 0.30))
    if league_key in STATIC_LDW:
        return STATIC_LDW[league_key]
    return 0.30                                            # uncoded league default

def score_player(player, ldw):
    total = 0.0
    for st in player.get('stints', []):
        days = st.get('duration_days', 0) or 0
        rec = RECENCY.get(st.get('season',''), 1.0)
        for comp, share in (st.get('competition_share', {}) or {}).items():
            if comp == 'domestic':
                w = league_weight(ldw, st.get('league_key'), st.get('season'))
                pos, size = st.get('domestic_league_finish'), st.get('league_size')
                q = (size - pos + 1)/size if (pos and size and size > 0) else 0.5
            else:
                w = CONTINENTAL.get(comp, 0.30)
                prog = None
                for pcx in st.get('parallel_competitions', []):
                    if pcx.get('competition_key') == comp:
                        prog = pcx.get('club_progress'); break
                q = PROGRESS.get(prog, 0.5) if prog else 0.5
            total += days * rec * share * w * q
    return total * SCALE

def main():
    ldw = load_per_season_ldw('per_season_ldw.csv')
    data = json.load(open('player_contexts.json', encoding='utf-8'))
    rows = []
    team_tot = defaultdict(list)
    for team, players in data['teams'].items():
        for p in players:
            sc = round(score_player(p, ldw), 3)
            rows.append((team, p.get('name',''), sc))
            team_tot[team].append(sc)
    with open('player_scores_reproduced.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['team','player','score'])
        w.writerows(sorted(rows))
    # team ranking by top-15 (the model's default mode)
    ranking = sorted(((t, sum(sorted(v, reverse=True)[:15])) for t,v in team_tot.items()),
                     key=lambda x: -x[1])
    print("Reproduced. Team ranking (top-15 squad strength):")
    for i,(t,s) in enumerate(ranking, 1):
        print(f"  {i:2}. {t:16} {s:6.1f}")
    print("\nWrote player_scores_reproduced.csv")

if __name__ == '__main__':
    main()
