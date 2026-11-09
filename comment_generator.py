
import csv
import json
from pathlib import Path

COMMENTS_FILE = Path("comments.txt")
CREATORS_FILE = Path("creators.csv")
STATE_FILE = Path("outreach_state.json")

MAX_OUTREACH = 125


def load_comments():
    return [
        line.strip()
        for line in COMMENTS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))

    return {"next_comment": 0, "total_posted": 0}


def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )


def main():
    comments = load_comments()

    if len(comments) != 25:
        print(f"Error: Expected 25 comments, found {len(comments)}")
        return

    state = load_state()

    if state["total_posted"] >= MAX_OUTREACH:
        print("125 outreach interactions completed.")
        return

    username = input("TikTok username: ").strip().lstrip("@")
    video_url = input("Public video URL: ").strip()
    country = input("Country: ").strip()
    niche = input("Creator niche: ").strip()

    if not username or not video_url:
        print("Username and video URL are required.")
        return

    with CREATORS_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        rows = list(csv.DictReader(file))

    if any(row["username"].lower() == username.lower() for row in rows):
        print("This creator is already recorded. Duplicate blocked.")
        return

    index = state["next_comment"]
    selected_comment = comments[index]

    print("\nSelected comment:")
    print(selected_comment)

    approval = input("\nDid you manually post this comment? (yes/no): ")

    if approval.strip().lower() != "yes":
        print("No progress recorded.")
        return

    with CREATORS_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            username,
            video_url,
            country,
            niche,
            "not_verified",
            selected_comment,
            "posted",
            ""
        ])

    state["next_comment"] = (index + 1) % 25
    state["total_posted"] += 1
    save_state(state)

    print(
        f"\nProgress: {state['total_posted']}/{MAX_OUTREACH}"
    )
    print("Comment sequence position:", state["next_comment"] + 1)


if __name__ == "__main__":
    main()
