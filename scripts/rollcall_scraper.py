"""
Roll Call FactBase – Social Posts Scraper
==========================================
Directly queries the WordPress REST API that powers the FactBase social feed.
No Selenium needed — this is much faster and more reliable.

Requirements:
    pip install requests pandas beautifulsoup4

Usage:
    python rollcall_scraper.py

Output:
    rollcall_social_posts.csv
"""

import time
import csv
import requests
from bs4 import BeautifulSoup

# ── Configuration ─────────────────────────────────────────────────────────────

BASE_URL    = "https://rollcall.com/wp-json/factbase/v1/twitter"
OUTPUT_FILE = "data/rollcall_social_posts.csv"
PAGE_DELAY  = 0.1       # polite pause between requests (seconds)
MAX_RETRIES = 5         # max retry attempts per page before giving up

# Set to a page number > 1 to resume from a specific page (e.g. 776).
# When resuming, the CSV will be opened in append mode so prior data is preserved.
START_PAGE  = 1

# Filter options — adjust as needed:
PLATFORM    = "all"     # "all", "twitter", or "truth social"
SORT        = "date"
SORT_ORDER  = "desc"    # "desc" = newest first, "asc" = oldest first

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Referer": "https://rollcall.com/factbase/trump/topic/social/",
}

# ── Text extraction ───────────────────────────────────────────────────────────

def extract_text(post: dict) -> str:
    """
    Pull plain text from a post record.
    Prefers the rendered HTML (post_html) since it has full content;
    falls back to the plain 'text' field.
    """
    html = post.get("social", {}).get("post_html", "")
    if html and html.strip() and html.strip() != "<p></p>":
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    return post.get("text", "").strip()


# ── Main scraper ──────────────────────────────────────────────────────────────

def fetch_page(session: requests.Session, page: int) -> dict:
    """
    Fetch a single page from the API with exponential-backoff retry.
    On each failure the wait doubles: 2s, 4s, 8s, 16s, 32s …
    Raises RuntimeError if all retries are exhausted.
    """
    params = {
        "platform":   PLATFORM,
        "sort":       SORT,
        "sort_order": SORT_ORDER,
        "page":       page,
        "format":     "json",
    }

    delay = PAGE_DELAY * 2  # starting retry delay (doubles on each attempt)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(BASE_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            if not (data.get("meta") and data.get("data") is not None):
                raise ValueError("Unexpected response structure")

            return data

        except Exception as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    f"Page {page} failed after {MAX_RETRIES} attempts: {e}"
                ) from e

            print(f"\n    Attempt {attempt} failed: {e}")
            print(f"    Retrying in {delay:.0f}s...", end=" ", flush=True)
            time.sleep(delay)
            delay *= 2  # exponential backoff


def scrape_all_posts(start_page: int = 1) -> list:
    """
    Paginate through the API starting from `start_page`.
    Returns a list of dicts with keys: content, platform, date, post_url, deleted.
    """
    all_posts = []
    page = start_page

    session = requests.Session()
    session.headers.update(HEADERS)

    while True:
        print(f"  -> Fetching page {page}...", end=" ", flush=True)

        try:
            data = fetch_page(session, page)
        except RuntimeError as e:
            print(f"\n  GIVING UP: {e}")
            break

        posts_on_page = data["data"]
        total_pages   = data["meta"].get("page_count", 1)
        total_hits    = data["meta"].get("total_hits", "?")

        if not posts_on_page:
            print("No posts returned. Stopping.")
            break

        print(f"got {len(posts_on_page)} posts  (page {page}/{total_pages}, total ~{total_hits})")

        for post in posts_on_page:
            all_posts.append({
                "content":  extract_text(post),
                "platform": post.get("platform", ""),
                "date":     post.get("date", ""),
                "post_url": post.get("post_url", ""),
                "deleted":  bool(post.get("deleted_flag")),
            })

        if page >= total_pages:
            print(f"\n  Done. Reached last page ({total_pages}).")
            break

        page += 1
        time.sleep(PAGE_DELAY)

    return all_posts


def save_to_csv(posts: list, filepath: str, append: bool = False) -> None:
    if not posts:
        print("No posts to save.")
        return

    fieldnames = ["content", "platform", "date", "post_url", "deleted"]
    mode = "a" if append else "w"

    with open(filepath, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not append:
            writer.writeheader()
        writer.writerows(posts)

    action = "Appended" if append else "Saved"
    print(f"\n  {action} {len(posts)} posts -> {filepath}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    resuming = START_PAGE > 1
    print(f"Starting scrape: platform={PLATFORM!r}, sort={SORT} {SORT_ORDER}")
    if resuming:
        print(f"Resuming from page {START_PAGE} (appending to existing CSV)\n")
    else:
        print()

    posts = scrape_all_posts(start_page=START_PAGE)
    save_to_csv(posts, OUTPUT_FILE, append=resuming)
    print("\nDone.")