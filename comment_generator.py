"""Prepare up to 10 personalized outreach comment drafts; does not publish them."""
import csv, json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CANDIDATES = ROOT / 'creator_candidates.csv'
CONTACTED = ROOT / 'creators.csv'
COMMENTS = ROOT / 'comments.txt'
QUEUE = ROOT / 'comment_queue.csv'
STATE = ROOT / 'outreach_state.json'
BATCH_LIMIT = 10
MAX_TRACKED = 125
QUEUE_FIELDS = ['username','profile_url','video_url','country','niche','comment','status','created_at_utc']


def read_csv(path):
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    if not CANDIDATES.exists():
        print('Missing creator_candidates.csv')
        return
    comments = [x.strip() for x in COMMENTS.read_text(encoding='utf-8').splitlines()
                if x.strip() and not x.lstrip().startswith('#')]
    if not comments:
        print('comments.txt is empty')
        return
    candidates = read_csv(CANDIDATES)
    contacted_rows = read_csv(CONTACTED)
    queued_rows = read_csv(QUEUE)
    contacted = {r.get('username','').strip().lower() for r in contacted_rows}
    already_queued = {r.get('username','').strip().lower() for r in queued_rows}
    state = json.loads(STATE.read_text()) if STATE.exists() else {'next_comment': 0}
    total_tracked = sum(1 for r in contacted_rows if r.get('status','').lower() == 'posted')
    if total_tracked >= MAX_TRACKED:
        print(f'Tracking limit reached: {MAX_TRACKED}.')
        return
    remaining = min(BATCH_LIMIT, MAX_TRACKED - total_tracked)
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    new_rows = []
    idx = int(state.get('next_comment', 0)) % len(comments)

    for c in candidates:
        username = c.get('username','').strip().lstrip('@')
        video = c.get('video_url','').strip()
        country = c.get('country','').strip()
        niche = c.get('niche','').strip().lower()
        if not username or not video or username.lower() in contacted or username.lower() in already_queued:
            continue
        if country.lower() not in {'usa','united states','canada','uk','united kingdom'}:
            continue
        if niche not in {'gym','fitness','workout','activewear'}:
            continue
        # Require explicit human confirmation in the candidate sheet; age is not inferred.
        if c.get('age_verified','').strip().lower() != 'yes':
            continue
        if c.get('human_content_confirmed','').strip().lower() != 'yes':
            continue
        new_rows.append({
            'username': username,
            'profile_url': c.get('profile_url','').strip(),
            'video_url': video,
            'country': country,
            'niche': niche,
            'comment': comments[idx],
            'status': 'draft',
            'created_at_utc': now,
        })
        already_queued.add(username.lower())
        idx = (idx + 1) % len(comments)
        if len(new_rows) >= remaining:
            break

    if new_rows:
        write_csv(QUEUE, queued_rows + new_rows, QUEUE_FIELDS)
        state['next_comment'] = idx
        STATE.write_text(json.dumps(state, indent=2), encoding='utf-8')
    print(f'Created {len(new_rows)} new comment drafts (maximum {BATCH_LIMIT} per run).')
    print(f'Queue: {QUEUE.name}')
    print('Publishing is not automated. Drafts must be posted manually in TikTok.')
    if not new_rows:
        print('No new eligible candidates. Add verified public creator details to creator_candidates.csv.')

if __name__ == '__main__':
    main()
