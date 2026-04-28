import csv
import requests
import time
import logging
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

CSV_FILE = "Task 2 - Intern.csv"
OUTPUT_FILE = "results.csv"
LOG_FILE = "app.log"
MAX_RETRIES = 3


# 🔹 Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


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
            logging.info(f"{status} - {url}")
            return {"url": url, "status": status, "error": ""}

        if attempt < MAX_RETRIES:
            time.sleep(1)
        else:
            logging.error(f"{error} - {url}")
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

    logging.info(f"Loaded {len(urls)} URLs from CSV")
    return urls


def save_results(results):
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Status Code", "Error"])

        for r in results:
            writer.writerow([r["url"], r["status"], r["error"]])

    logging.info(f"Results saved to {OUTPUT_FILE}")


def print_summary(results):
    total = len(results)
    success = sum(1 for r in results if r["status"])
    failed = total - success

    status_counter = Counter(r["status"] for r in results if r["status"])
    error_counter = Counter(r["error"] for r in results if r["error"])

    logging.info("===== SUMMARY =====")
    logging.info(f"Total URLs: {total}")
    logging.info(f"Successful: {success}")
    logging.info(f"Failed: {failed}")

    logging.info("Status Code Breakdown:")
    for code, count in status_counter.items():
        logging.info(f"{code}: {count}")

    if error_counter:
        logging.info("Error Breakdown:")
        for err, count in error_counter.items():
            logging.info(f"{err}: {count}")


def main():
    urls = read_urls()
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_status_code, url) for url in urls]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    save_results(results)
    print_summary(results)


if __name__ == "__main__":
    main()