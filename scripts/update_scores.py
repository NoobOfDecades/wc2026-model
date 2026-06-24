#!/usr/bin/env python3
"""
WC2026 Score Updater
Fetches latest results from ESPN, patches index.html, commits + pushes.
  - dev branch  → auto-push (no prompt)
  - main branch → shows changes, asks confirmation before pushing to production
"""
import subprocess, json, re, sys, os
from datetime import datetime, timezone, timedelta

try:
    import requests
except ImportError:
    subprocess.run([sys.executable,'-m','pip','install','requests','--break-system-packages','-q'])
    import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR   = os.path.dirname(SCRIPT_DIR)
HTML_PATH  = os.path.join(REPO_DIR, 'index.html')

# ESPN WC2026 API — no key required
ESPN_URL = ('https://site.api.espn.com/apis/site/v2/sports/soccer/'
            'fifa.worldcup/scoreboard?dates=20260601-20260715&limit=200')

# Map ESPN display names → our team keys
ESPN_MAP = {
    'france':'FRANCE','england':'ENGLAND','spain':'SPAIN','brazil':'BRAZIL',
    'netherlands':'NETHERLANDS','portugal':'PORTUGAL','germany':'GERMANY',
    'argentina':'ARGENTINA','belgium':'BELGIUM','uruguay':'URUGUAY',
    'norway':'NORWAY','croatia':'CROATIA','italy':'ITALY','mexico':'MEXICO',
    'united states':'USA','usa':'USA','united states of america':'USA',
    'south korea':'SOUTH_KOREA','korea republic':'SOUTH_KOREA',
    'japan':'JAPAN','australia':'AUSTRALIA','senegal':'SENEGAL',
    'morocco':'MOROCCO','nigeria':'NIGERIA','ghana':'GHANA',
    'cameroon':'CAMEROON','egypt':'EGYPT','algeria':'ALGERIA',
    'south africa':'SOUTH_AFRICA','cote d\'ivoire':'IVORY_COAST',
    'ivory coast':'IVORY_COAST','canada':'CANADA','colombia':'COLOMBIA',
    'chile':'CHILE','ecuador':'ECUADOR','paraguay':'PARAGUAY',
    'uruguay':'URUGUAY','venezuela':'VENEZUELA','peru':'PERU',
    'saudi arabia':'SAUDI_ARABIA','iran':'IRAN','iraq':'IRAQ',
    'qatar':'QATAR','uzbekistan':'UZBEKISTAN','jordan':'JORDAN',
    'turkey':'TURKEY','austria':'AUSTRIA','switzerland':'SWITZERLAND',
    'czechia':'CZECHIA','czech republic':'CZECHIA','scotland':'SCOTLAND',
    'sweden':'SWEDEN','denmark':'DENMARK','poland':'POLAND',
    'serbia':'SERBIA','hungary':'HUNGARY','ukraine':'UKRAINE',
    'russia':'RUSSIA','new zealand':'NEW_ZEALAND','dr congo':'CONGO_DR',
    'congo dr':'CONGO_DR','democratic republic of the congo':'CONGO_DR',
    'panama':'PANAMA','haiti':'HAITI','costa rica':'COSTA_RICA',
    'honduras':'HONDURAS','cape verde':'CAPE_VERDE','curacao':'CURACAO',
    'tunisia':'TUNISIA','mali':'MALI','angola':'ANGOLA',
    'bosnia & herzegovina':'BOSNIA','bosnia-herzegovina':'BOSNIA',
    'bosnia and herzegovina':'BOSNIA','bosnia':'BOSNIA',
    'china':'CHINA','india':'INDIA','indonesia':'INDONESIA',
    'thailand':'THAILAND','vietnam':'VIETNAM',
}

def espn_to_key(name):
    return ESPN_MAP.get(name.lower().strip())

def fetch_scores():
    try:
        r = requests.get(ESPN_URL, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"  ESPN fetch failed: {e}")
        return []
    results = []
    for ev in data.get('events', []):
        comp = ev.get('competitions', [{}])[0]
        status = comp.get('status', {})
        if not status.get('type', {}).get('completed', False):
            continue
        teams = comp.get('competitors', [])
        if len(teams) < 2:
            continue
        home = next((t for t in teams if t.get('homeAway') == 'home'), teams[0])
        away = next((t for t in teams if t.get('homeAway') == 'away'), teams[1])
        h_name = home.get('team', {}).get('displayName', '')
        a_name = away.get('team', {}).get('displayName', '')
        h_key  = espn_to_key(h_name)
        a_key  = espn_to_key(a_name)
        if not h_key or not a_key:
            print(f"  Unmapped teams: '{h_name}' / '{a_name}'")
            continue
        try:
            h_score = int(home.get('score', -1))
            a_score = int(away.get('score', -1))
        except (ValueError, TypeError):
            continue
        if h_score < 0 or a_score < 0:
            continue
        # parse date (UTC → SAST +2)
        date_str = comp.get('date', '')
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            dt = None
        results.append({'home': h_key, 'away': a_key,
                        'hs': h_score, 'as': a_score, 'dt': dt})
    return results

def load_html():
    with open(HTML_PATH, encoding='utf-8') as f:
        return f.read()

def patch_fixtures(html, scores):
    # Match on team pair — order-independent (home/away might be swapped in our data)
    score_lookup = {}
    for s in scores:
        score_lookup[(s['home'], s['away'])] = (s['hs'], s['as'])
        score_lookup[(s['away'], s['home'])] = (s['as'], s['hs'])

    def replacer(m):
        a, b, iso, hs, as_ = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        if hs != 'null' and as_ != 'null':
            return m.group(0)  # already scored, skip
        key = (a, b)
        if key in score_lookup:
            ns, na = score_lookup[key]
            return f'["{a}", "{b}", "{iso}", {ns}, {na}'
        return m.group(0)

    pattern = r'\["([A-Z_]+)", "([A-Z_]+)", "([^"]+)", (null|\d+), (null|\d+)'
    new_html, n = re.subn(pattern, replacer, html)
    return new_html, n

def git_branch():
    r = subprocess.run(['git','branch','--show-current'],
                       capture_output=True, text=True, cwd=REPO_DIR)
    return r.stdout.strip()

def git_push(branch, msg):
    subprocess.run(['git','add','index.html'], cwd=REPO_DIR, check=True)
    subprocess.run(['git','commit','-m', msg], cwd=REPO_DIR, check=True)
    subprocess.run(['git','push','origin', branch], cwd=REPO_DIR, check=True)

def main():
    print("=== WC2026 Score Updater ===")
    print(f"HTML: {HTML_PATH}")
    branch = git_branch()
    print(f"Branch: {branch}")

    print("\nFetching scores from ESPN...")
    scores = fetch_scores()
    print(f"Completed matches found: {len(scores)}")

    html = load_html()
    new_html, total = patch_fixtures(html, scores)

    # count how many were actually unscored before
    unscored_before = len(re.findall(r'"[A-Z_]+", "[A-Z_]+", "[^"]+", null, null', html))
    newly_scored = len(re.findall(r'"[A-Z_]+", "[A-Z_]+", "[^"]+", null, null', new_html))
    updates = unscored_before - newly_scored

    print(f"Previously unscored: {unscored_before}")
    print(f"Newly scored: {updates}")

    if updates == 0:
        print("\nNo new results to add. Nothing to push.")
        return

    # Show what changed
    old_nulls = re.findall(r'\["([A-Z_]+)", "([A-Z_]+)", "[^"]+", null, null', html)
    new_nulls = set(re.findall(r'"([A-Z_]+)", "([A-Z_]+)", "[^"]+", null, null', new_html))
    print("\nMatches being updated:")
    for a, b in old_nulls:
        if (a, b) not in new_nulls and (b, a) not in new_nulls:
            key = (a,b) if (a,b) in {(s['home'],s['away']) for s in scores} else (b,a)
            sc = {(s['home'],s['away']):(s['hs'],s['as']) for s in scores}
            sc.update({(s['away'],s['home']):(s['as'],s['hs']) for s in scores})
            if key in sc:
                print(f"  {a} {sc[key][0]}-{sc[key][1]} {b}")
            else:
                print(f"  {a} vs {b}")

    # Update build stamp
    from datetime import datetime
    import pytz
    try:
        sast = pytz.timezone('Africa/Johannesburg')
        stamp = datetime.now(sast).strftime('%Y-%m-%d %H:%M SAST')
    except:
        stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    new_html = re.sub(r'const BUILD_STAMP="[^"]*";', f'const BUILD_STAMP="{stamp}";', new_html)

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"\nHTML updated. Build stamp: {stamp}")

    commit_msg = f"scores: bake {updates} result(s) — {stamp}"

    if branch == 'main':
        print(f"\n⚠️  You are on MAIN (production → model26.xyz)")
        confirm = input("Push to production? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Aborted. HTML is updated locally but not pushed.")
            print("Run 'git checkout dev && python3 scripts/update_scores.py' to push to preview first.")
            return
    else:
        print(f"\nDev branch — auto-pushing to preview...")

    git_push(branch, commit_msg)
    print(f"\n✅ Pushed to {branch}.")
    if branch == 'main':
        print("   Live at: https://model26.xyz")
    else:
        print("   Preview URL: check Cloudflare Pages dashboard for your branch preview link.")

if __name__ == '__main__':
    main()
