# Outreachy Round 32 — Wikimedia Lusophone Technological Wishlist
## Task 2: URL Status Code Checker with Python

**Applicant:** bobaigwa  
**Program:** [Outreachy](https://www.outreachy.org/) — Round 32  
**Organization:** [Wikimedia Brasil](https://www.wmnobrasil.org/)  
**Task Reference:** [T418286 on Wikimedia Phabricator](https://phabricator.wikimedia.org/T418286)

---

## Overview

This repository contains my submission for **Task 2** of the Outreachy Round 32 contribution phase for the Wikimedia Brasil project: *Addressing the Lusophone Technological Wishlist Proposals*.

The task involves writing a Python script that reads a list of URLs from a `.csv` file, sends an HTTP request to each one, and prints the response status code in a clean, human-readable format.

---

## Task Objective

> Read a list of URLs from a `.csv` file and print the HTTP status code of each URL's response in the following format:
>
> `(STATUS_CODE) URL`

**Example output:**
```
(200) https://www.nytimes.com/1999/07/04/sports/women-s-world-cup-sissi-of-brazil-has-right-stuff-with-left-foot.html
(404) http://www.bayareasportsdrive.com/soccer/sissi.htm
(ERROR: Connection failed) http://jogandocomelas.com.br/rosana-augusto-...
```

---

## Dataset

**File:** `Task 2 - Intern.csv`

The input CSV contains 160 URLs referencing articles, profiles, and media about Brazilian women's football players and related topics. Each row contains one URL in the first column.

---

## Implementation

**File:** `task2.py`

The solution is a single Python script with no external dependencies beyond the `requests` library. The key logic:

1. **CSV parsing** — Uses Python's built-in `csv` module to read the input file row by row, extracting the URL from the first column and skipping any empty or non-URL rows gracefully.

2. **HEAD request first** — Sends a `HEAD` request instead of a full `GET` request. This is more efficient because the server only returns headers and a status code without sending the full page body, reducing bandwidth and response time.

3. **GET fallback** — If the server responds with `405 Method Not Allowed` (some servers do not support `HEAD`), the script automatically retries with a `GET` request to ensure an accurate status code is always retrieved.

4. **Error handling** — Network failures, timeouts, and other request exceptions are caught and reported clearly instead of crashing the script, allowing all URLs to be checked in a single run.

```python
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
        return response.status_code
    except requests.exceptions.ConnectionError:
        return "ERROR: Connection failed"
    except requests.exceptions.Timeout:
        return "ERROR: Timeout"
    except requests.exceptions.RequestException as e:
        return f"ERROR: {e}"
```

---

## Common Status Codes You Will See

| Code | Meaning |
|---|---|
| `200` | OK — page is live and accessible |
| `301` / `302` | Redirected — URL moved, followed automatically |
| `403` | Forbidden — server refused access |
| `404` | Not Found — page no longer exists |
| `410` | Gone — page was permanently removed |
| `ERROR: Timeout` | Server took too long to respond |
| `ERROR: Connection failed` | Domain does not exist or is unreachable |

---

## How to Run

**Requirements:** Python 3.6+ and the `requests` library.

```bash
# 1. Clone the repository
git clone https://github.com/Brace1000/outreachy-wikimedia-microtasks.git
cd outreachy-wikimedia-microtasks/task2

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install requests

# 4. Run the script
python3 task2.py
```

Make sure `Task 2 - Intern.csv` is in the same directory as `task2.py` before running.

---

## Project Structure

```
task2/
├── task2.py            # Main Python script
└── Task 2 - Intern.csv # Input CSV file containing the list of URLs
```

---

## Project Context

The [Lusophone Technological Wishlist](https://meta.wikimedia.org/wiki/Lista_de_desejos_tecnol%C3%B3gicos_da_lusofonia) is a survey conducted across Portuguese-speaking Wikimedia communities to identify technological innovations and tool improvements that could benefit users. This Outreachy project aims to address the top proposals from that survey.

This task specifically relates to URL verification — a key step in maintaining the reliability of references and external links across Wikimedia articles in Portuguese.

---

## License

This project follows the contribution guidelines of Wikimedia Brasil and Outreachy Round 32.  
Content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).