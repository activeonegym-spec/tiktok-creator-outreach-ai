# Operating instructions
1. Use the generated TikTok search links to locate public creators.
2. Enter each candidate in `creator_candidates.csv` with username, profile URL, video URL, country, niche, and verified fields.
3. Do not infer a person's age from their face, body, voice, or content. Use only reliable public confirmation; otherwise leave `age_verified` blank.
4. Run `python creator_finder.py`, then `python comment_generator.py`.
5. Review the generated queue, then manually post only relevant comments in TikTok.
6. Mark each actually posted comment using `python mark_posted.py USERNAME`.
7. Maximum draft batch is 10 per run; 125 is a tracking ceiling, not a guarantee or recommended posting target.
