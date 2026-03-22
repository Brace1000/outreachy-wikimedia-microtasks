import csv
import requests

# Read URLs from the CSV file and print their HTTP status codes.
# Output format: (STATUS_CODE) URL
# e.g. (200) https://www.nytimes.com/...

CSV_FILE = "Task 2 - Intern.csv"

def get_status_code(url):
    """
    Send a HEAD request to the URL and return its HTTP status code.
    Falls back to a GET request if HEAD is not supported.
    Returns a string like "ERROR: <reason>" if the request fails entirely.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; OutreachyBot/1.0; "
            "+https://github.com/Brace1000/outreachy-wikimedia-microtasks)"
        )
    }
    try:
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        # Some servers return 405 (Method Not Allowed) for HEAD — fall back to GET
        if response.status_code == 405:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        return response.status_code
    except requests.exceptions.ConnectionError:
        return "ERROR: Connection failed"
    except requests.exceptions.Timeout:
        return "ERROR: Timeout"
    except requests.exceptions.RequestException as e:
        return f"ERROR: {e}"


def main():
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            url = row[0].strip()
            # Skip empty lines or header rows that don't look like URLs
            if not url or not url.startswith("http"):
                continue
            status = get_status_code(url)
            print(f"({status}) {url}")


if __name__ == "__main__":
    main()