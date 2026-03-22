# Outreachy Round 32 — Wikimedia Lusophone Technological Wishlist
## Task 1: JSON Data Manipulation with JavaScript

**Applicant:** bobaigwa  
**Program:** [Outreachy](https://www.outreachy.org/) — Round 32  
**Organization:** [Wikimedia Brasil](https://www.wmnobrasil.org/)  
**Task Reference:** [T418285 on Wikimedia Phabricator](https://phabricator.wikimedia.org/T418285)

---

## Overview

This repository contains my submission for **Task 1** of the Outreachy Round 32 contribution phase for the Wikimedia Brasil project: *Addressing the Lusophone Technological Wishlist Proposals*.

The task involves writing a JavaScript script that reads a structured JSON dataset of Wikipedia articles and renders the information in a clean, human-readable format inside an HTML page.

---

## Task Objective

> Parse a JSON array of Wikipedia article metadata and display each entry in the following format:
>
> `Article "TITLE" (Page ID PAGEID) was created at MONTH DAY, YEAR.`

**Example output:**
```
Article "André Baniwa" (Page ID 6682420) was created at September 13, 2021.
```

---

## Dataset

The input data consists of 12 Wikipedia articles related to Indigenous Brazilian figures and leaders, each containing:

| Field | Description |
|---|---|
| `title` | Title of the Wikipedia article |
| `page_id` | Unique Wikipedia page identifier |
| `creation_date` | Date the article was created (`YYYY-MM-DD`) |

---

## Implementation

**File:** `Task-1-Intern.html`

The solution is implemented as a single self-contained HTML file with embedded JavaScript. The key logic:

1. **Date parsing** — The `creation_date` string (`YYYY-MM-DD`) is split into its components and passed to `new Date(year, month-1, day)` using local time construction. This avoids a common timezone offset bug where parsing ISO strings as UTC can shift the displayed date back by one day.

2. **Rendering** — The script iterates over each article object using `Array.forEach()`, builds the required sentence, and dynamically creates a `<p>` element that is appended to the `#results` div.

```javascript
function formatDate(dateStr) {
  const [year, month, day] = dateStr.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  return date.toLocaleDateString("en-US", {
    year:  "numeric",
    month: "long",
    day:   "numeric",
  });
}

const resultsDiv = document.getElementById("results");

data.forEach(function (article) {
  const formattedDate = formatDate(article.creation_date);
  const p = document.createElement("p");
  p.textContent =
    `Article "${article.title}" (Page ID ${article.page_id}) was created at ${formattedDate}.`;
  resultsDiv.appendChild(p);
});
```

---

## Output

```
Article "André Baniwa" (Page ID 6682420) was created at September 13, 2021.
Article "Benki Piyãko" (Page ID 4246775) was created at December 10, 2013.
Article "Célia Xakriabá" (Page ID 5882073) was created at December 3, 2018.
Article "Chirley Pankará" (Page ID 6977673) was created at October 5, 2022.
Article "Cristine Takuá" (Page ID 7069044) was created at February 16, 2023.
Article "Eliane Potiguara" (Page ID 2119511) was created at January 28, 2009.
Article "Jaider Esbell" (Page ID 6714407) was created at October 9, 2021.
Article "Jerônimo Rodrigues" (Page ID 6977117) was created at October 4, 2022.
Article "Nanblá Gakran" (Page ID 6935831) was created at August 2, 2022.
Article "Sônia Guajajara" (Page ID 4908665) was created at November 13, 2015.
Article "Vãngri Kaingáng" (Page ID 5886895) was created at December 12, 2018.
Article "Zezico Guajajara" (Page ID 6549130) was created at April 10, 2021.
```

---

## How to Run

No build tools or dependencies required.

1. Clone or download this repository
2. Open `Task-1-Intern.html` in any modern web browser
3. The results render immediately on page load

---

## Project Context

The [Lusophone Technological Wishlist](https://meta.wikimedia.org/wiki/Lista_de_desejos_tecnol%C3%B3gicos_da_lusofonia) is a survey conducted across Portuguese-speaking Wikimedia communities to identify technological innovations and tool improvements that could benefit users. This Outreachy project aims to address the top proposals from that survey.

---

## License

This project follows the contribution guidelines of Wikimedia Brasil and Outreachy Round 32.  
Content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).