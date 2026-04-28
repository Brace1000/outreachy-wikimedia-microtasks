# Outreachy Task 1 — Article Renderer (Improved Version)

## 👤 Applicant
bobaigwa

## 📌 Project Context
This project was completed as part of Outreachy Round 32 for the Wikimedia Brasil project:
**Addressing the Lusophone Technological Wishlist Proposals**

---

## 📖 Overview
This project is a JavaScript-based article renderer that processes a JSON dataset of Wikipedia articles and displays them in a structured, readable format in a web page.

The application evolved through multiple improvements during the contribution phase, focusing on:
- Data handling
- User interaction
- Code structure
- UI/UX improvements

---

## 🚀 Features

### 1. Article Rendering
Displays Wikipedia article metadata in a human-readable format:
- Title
- Page ID
- Creation date

---

### 2. Sorting Functionality
Users can dynamically sort articles by:
- Newest first
- Oldest first

---

### 3. Data Validation
Ensures only valid article objects are processed:
- Checks required fields
- Prevents runtime errors from malformed data

---

### 4. Modular Architecture
Code is structured into reusable functions:
- Sorting logic
- Validation logic
- Rendering logic
- DOM creation logic

---

### 5. Improved UI/UX
- Card-based layout for readability
- Summary counter showing number of articles displayed
- Empty state message for better feedback

---

## 🧠 Architecture Overview

The application follows a simple modular structure:

- **Utilities**
  - `formatDate()` → formats date strings
  - `isValidArticle()` → validates input data
  - `sortData()` → handles sorting logic

- **UI Layer**
  - `createArticleCard()` → builds UI elements
  - `renderArticles()` → renders processed data

- **Controller**
  - `updateView()` → manages sorting + rendering flow
  - `init()` → initializes event listeners

---

## 🔄 Data Flow

1. Load JSON data
2. User selects sorting option
3. Data is sorted
4. Invalid entries are filtered out
5. Valid articles are rendered as cards
6. UI summary is updated

---

## 🛠 How to Run

1. Open `index.html` in any modern browser
2. The application loads automatically
3. Use dropdown to change sorting order

No dependencies required.

---

## 📈 Improvements Made During Contributions

This project evolved through incremental improvements:

- Added sorting functionality
- Introduced data validation layer
- Refactored into modular functions
- Improved UI with card layout
- Added summary and empty state handling

---

## 🎯 Key Learning Outcomes

- DOM manipulation in JavaScript
- Data validation techniques
- Modular code design
- Event-driven UI updates
- Improving usability through UI feedback

---

## 📜 License
Part of Outreachy contribution work for Wikimedia Brasil (CC BY-SA 4.0 where applicable)