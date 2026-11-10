import csv
from pathlib import Path
CANDIDATES_FILE=Path(__file__).with_name('creator_candidates.csv')
CONTACTED_FILE=Path(__file__).with_name('creators.csv')
ALLOWED_COUNTRIES={'united states','usa','canada','united kingdom','uk'}
ALLOWED_NICHES={'gym','fitness','workout','activewear'}
def read(path):
    if not path.exists(): return []
    with path.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def main():
    candidates=read(CANDIDATES_FILE); contacted=read(CONTACTED_FILE)
    done={r.get('username','').strip().lower() for r in contacted}
    seen=set(); approved=[]
    for c in candidates:
        u=c.get('username','').strip().lstrip('@'); country=c.get('country','').strip().lower(); niche=c.get('niche','').strip().lower()
        if not u or not c.get('video_url','').strip() or u.lower() in done or u.lower() in seen: continue
        if country not in ALLOWED_COUNTRIES or niche not in ALLOWED_NICHES: continue
        if c.get('age_verified','').strip().lower()!='yes' or c.get('human_content_confirmed','').strip().lower()!='yes': continue
        seen.add(u.lower()); approved.append(c)
    print(f'Eligible unique candidates: {len(approved)}')
    for c in approved:
        print(f"@{c['username']} | {c['country']} | {c['niche']} | {c['video_url']}")
    print('Next: python comment_generator.py (creates up to 10 drafts; does not publish).')
if __name__=='__main__': main()
