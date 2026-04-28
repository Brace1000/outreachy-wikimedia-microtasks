import csv
import requests
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

CSV_FILE = "Task 2 - Intern.csv"
OUTPUT_FILE = "results.csv"
MAX_RETRIES = 3


def fetch_url(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; OutreachyBot/1.0; "
            "+https://github.com/Brace1000/outreachy-wikimedia-microtasks)"
        )
    }

    try:
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)

        if response.status_code == 405:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)

        return response.status_code, ""

    except requests.exceptions.ConnectionError:
        return None, "Connection failed"

    except requests.exceptions.Timeout:
        return None, "Timeout"

    except requests.exceptions.RequestException as e:
        return None, str(e)


def get_status_code(url):
    for attempt in range(1, MAX_RETRIES + 1):
        status, error = fetch_url(url)

        if status is not None:
            return {"url": url, "status": status, "error": ""}

        if attempt < MAX_RETRIES:
            time.sleep(1)
        else:
            return {"url": url, "status": "", "error": error}


def read_urls():
    urls = []

    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue

            url = row[0].strip()

            if url.startswith("http"):
                urls.append(url)

    return urls


def save_results(results):
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Status Code", "Error"])

        for r in results:
            writer.writerow([r["url"], r["status"], r["error"]])


def print_summary(results):
    total = len(results)
    success = sum(1 for r in results if r["status"])
    failed = total - success

    status_counter = Counter(r["status"] for r in results if r["status"])
    error_counter = Counter(r["error"] for r in results if r["error"])

    print("\n===== SUMMARY =====")
    print(f"Total URLs: {total}")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")

    print("\nStatus Code Breakdown:")
    for code, count in status_counter.items():
        print(f"{code}: {count}")

    if error_counter:
        print("\nError Breakdown:")
        for err, count in error_counter.items():
            print(f"{err}: {count}")


def main():
    urls = read_urls()
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_status_code, url) for url in urls]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            if result["error"]:
                print(f"(ERROR: {result['error']}) {result['url']}")
            else:
                print(f"({result['status']}) {result['url']}")

    save_results(results)
    print_summary(results)


if __name__ == "__main__":
    main()