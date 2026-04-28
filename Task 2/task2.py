import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import time

CSV_FILE = "Task 2 - Intern.csv"
MAX_RETRIES = 2
TIMEOUT = 10
MAX_WORKERS = 10


def fetch_url(session, url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; OutreachyBot/1.0; "
            "+https://github.com/Brace1000/outreachy-wikimedia-microtasks)"
        )
    }

    try:
        response = session.head(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)

        if response.status_code == 405:
            response = session.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)

        return response.status_code

    except requests.exceptions.Timeout:
        return "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return "CONNECTION_ERROR"
    except requests.exceptions.RequestException:
        return "REQUEST_ERROR"


def get_status_with_retry(session, url):
    for attempt in range(MAX_RETRIES + 1):
        result = fetch_url(session, url)

        if isinstance(result, int):
            return result

        if attempt < MAX_RETRIES:
            time.sleep(1)  # simple backoff

    return result  # final error after retries


def read_urls(file_path):
    urls = []

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not row:
                continue

            url = row[0].strip()

            if url.startswith("http"):
                urls.append(url)

    return urls


def process_urls(urls):
    results = []

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(get_status_with_retry, session, url): url
                for url in urls
            }

            for future in as_completed(futures):
                url = futures[future]
                status = future.result()

                results.append((status, url))
                print(f"({status}) {url}")

    return results


def summarize_results(results):
    counter = Counter()

    for status, _ in results:
        counter[status] += 1

    print("\n📊 Summary Report")
    print("-" * 30)

    total = sum(counter.values())
    print(f"Total URLs: {total}")

    for key, value in counter.items():
        print(f"{key}: {value}")


def main():
    urls = read_urls(CSV_FILE)

    print(f"Processing {len(urls)} URLs...\n")

    results = process_urls(urls)

    summarize_results(results)


if __name__ == "__main__":
    main()