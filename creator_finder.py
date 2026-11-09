
import csv
from pathlib import Path

CANDIDATES_FILE = Path("creator_candidates.csv")
CONTACTED_FILE = Path("creators.csv")

ALLOWED_COUNTRIES = {
    "United States",
    "USA",
    "Canada",
    "United Kingdom",
    "UK"
}

ALLOWED_NICHES = {
    "gym",
    "fitness",
    "workout",
    "activewear"
}


def create_template():
    if not CANDIDATES_FILE.exists():
        with CANDIDATES_FILE.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
                "username",
                "profile_url",
                "video_url",
                "country",
                "niche",
                "age",
                "age_verified",
                "human_content_confirmed"
            ])
        print("Candidate template created.")
        return True
    return False


def read_csv(path):
    if not path.exists():
        return []

    with path.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def main():
    if create_template():
        print("Add public creator details to creator_candidates.csv.")
        return

    candidates = read_csv(CANDIDATES_FILE)
    contacted = read_csv(CONTACTED_FILE)

    contacted_usernames = {
        row.get("username", "").strip().lower()
        for row in contacted
    }

    seen = set()
    approved = []

    for creator in candidates:
        username = creator.get("username", "").strip()
        country = creator.get("country", "").strip()
        niche = creator.get("niche", "").strip().lower()

        if not username or not creator.get("video_url", "").strip():
            continue

        if username.lower() in contacted_usernames:
            continue

        if username.lower() in seen:
            continue

        if country not in ALLOWED_COUNTRIES:
            continue

        if niche not in ALLOWED_NICHES:
            continue

        if creator.get("age_verified", "").lower() != "yes":
            continue

        if creator.get("human_content_confirmed", "").lower() != "yes":
            continue

        seen.add(username.lower())
        approved.append(creator)

    print(f"\nPotential creators for manual review: {len(approved)}")

    for creator in approved:
        print("\nUsername:", creator["username"])
        print("Country:", creator["country"])
        print("Niche:", creator["niche"])
        print("Video:", creator["video_url"])
        print("Age:", creator["age"])
        print("Review before outreach.")


if __name__ == "__main__":
    main()
