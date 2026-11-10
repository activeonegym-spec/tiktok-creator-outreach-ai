"""Mark a draft as posted after you publish it yourself in TikTok."""
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
QUEUE = ROOT / 'comment_queue.csv'
CREATORS = ROOT / 'creators.csv'
QFIELDS = ['username','profile_url','video_url','country','niche','comment','status','created_at_utc']
CFIELDS = ['username','video_url','country','niche','age_verified','comment_used','status','date_contacted']

def read(path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def write(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
def main():
    if len(sys.argv) != 2:
        print('Usage: python mark_posted.py USERNAME'); return
    name=sys.argv[1].lstrip('@').lower(); rows=read(QUEUE); found=None
    for r in rows:
        if r.get('username','').lower()==name and r.get('status')=='draft':
            r['status']='posted'; found=r; break
    if not found:
        print('No matching draft found (or it is already marked).'); return
    write(QUEUE, rows, QFIELDS)
    old=read(CREATORS)
    if not any(r.get('username','').lower()==name for r in old):
        old.append({'username':found['username'],'video_url':found['video_url'],'country':found['country'],
                    'niche':found['niche'],'age_verified':'yes','comment_used':found['comment'],
                    'status':'posted','date_contacted':found['created_at_utc']})
        write(CREATORS, old, CFIELDS)
    print(f"Marked @{found['username']} as posted. Only do this after you posted it yourself.")
if __name__=='__main__': main()
