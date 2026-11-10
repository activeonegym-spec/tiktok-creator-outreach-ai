# TikTok Creator Outreach AI — 10-draft test

This project helps organize public creator discovery and prepare outreach comments. **It does not log in to TikTok, control Chrome, or publish comments.** TikTok publishing must be done manually; this avoids unattended bulk-commenting and account-risky automation.

## What it does
- Creates TikTok search links from `search_keywords.txt`.
- Filters candidate rows for USA/Canada/UK and gym/fitness/workout/activewear.
- Requires explicit `age_verified=yes` and `human_content_confirmed=yes` fields; age is never guessed from appearance.
- Removes duplicate usernames already contacted or queued.
- Rotates through the 25 comments in `comments.txt`.
- Generates up to **10 comment drafts per run** in `comment_queue.csv`.
- Tracks posted items after you manually publish and run `python mark_posted.py USERNAME`.
- Stops preparing more drafts when 125 posted interactions are recorded.

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract this ZIP.
3. Open the folder, then open Command Prompt in that folder.
4. Run `python search_links.py` and open `search_links.md` to find creators.
5. Fill `creator_candidates.csv` with public creator details. Set `age_verified` and `human_content_confirmed` to `yes` only when you have reliable public confirmation.
6. Run `python creator_finder.py` to see eligible candidates.
7. Run `python comment_generator.py` to create up to 10 drafts.
8. Post suitable comments yourself in TikTok. After each one, run `python mark_posted.py username` (without @ is fine).

## Files
- `creator_candidates.csv`: candidate input sheet.
- `comment_queue.csv`: generated drafts and their status.
- `creators.csv`: manually posted/contacted history.
- `outreach_state.json`: comment rotation position.
- `search_links.md`: generated TikTok search links.

## Schedule
The GitHub Actions workflow can generate search links and run candidate filtering on the configured schedule (6–10 PM Pakistan time). It does not publish comments.
