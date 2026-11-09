
from pathlib import Path
from urllib.parse import quote_plus

KEYWORDS_FILE = Path("search_keywords.txt")
OUTPUT_FILE = Path("search_links.md")


def main():
    if not KEYWORDS_FILE.exists():
        print("search_keywords.txt not found.")
        return

    keywords = [
        line.strip()
        for line in KEYWORDS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        file.write("# TikTok Creator Search Links\n\n")

        for keyword in keywords:
            url = "https://www.tiktok.com/search?q=" + quote_plus(keyword)

            file.write(f"## {keyword}\n")
            file.write(f"{url}\n\n")

    print(f"Created {len(keywords)} TikTok search links.")
    print("Open search_links.md to use them.")


if __name__ == "__main__":
    main()
