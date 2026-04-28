import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

CSV_FILE = "Task 2 - Intern.csv"
OUTPUT_FILE = "results.csv"


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

        return {
            "url": url,
            "status": response.status_code,
            "error": ""
        }

    except requests.exceptions.ConnectionError:
        return {"url": url, "status": "", "error": "Connection failed"}

    except requests.exceptions.Timeout:
        return {"url": url, "status": "", "error": "Timeout"}

    except requests.exceptions.RequestException as e:
        return {"url": url, "status": "", "error": str(e)}


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

        # header
        writer.writerow(["URL", "Status Code", "Error"])

        for r in results:
            writer.writerow([r["url"], r["status"], r["error"]])


def main():
    urls = read_urls()
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_status_code, url) for url in urls]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            # console output
            if result["error"]:
                print(f"(ERROR: {result['error']}) {result['url']}")
            else:
                print(f"({result['status']}) {result['url']}")

    # save to CSV
    save_results(results)


if __name__ == "__main__":
    main()