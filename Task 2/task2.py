import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

CSV_FILE = "Task 2 - Intern.csv"

def get_status_code(url):
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
        return f"({response.status_code}) {url}"
    except requests.exceptions.ConnectionError:
        return f"(ERROR: Connection failed) {url}"
    except requests.exceptions.Timeout:
        return f"(ERROR: Timeout) {url}"
    except requests.exceptions.RequestException as e:
        return f"(ERROR: {e}) {url}"


def main():
    urls = []

    # Read CSV
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            url = row[0].strip()
            if url.startswith("http"):
                urls.append(url)

    # Run requests concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_status_code, url) for url in urls]

        for future in as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    main()