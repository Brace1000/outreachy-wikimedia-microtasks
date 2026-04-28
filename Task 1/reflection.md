# Reflection — Outreachy Task 1 Contribution Journey

## Overview
During this task, I worked on building a JavaScript-based article renderer that processes JSON data and displays it in a structured format. Over time, I improved the project through multiple incremental contributions, focusing on functionality, code quality, and user experience.

---

## What I Learned

### 1. Data Handling in JavaScript
I learned how to safely process JSON data and handle real-world issues such as missing or malformed fields. This helped me understand the importance of validating input before rendering it.

---

### 2. Importance of Code Structure
At the beginning, my code was functional but not well-organized. Through refactoring, I learned how separating logic into functions (validation, sorting, rendering) improves readability and maintainability.

---

### 3. Event-Driven UI Updates
I improved my understanding of how user interactions (like dropdown selection) can dynamically update the UI without reloading the page.

---

## Challenges I Faced

### 1. Handling Date Formatting Correctly
I initially faced issues with date parsing and display formats. I solved this by explicitly constructing Date objects using local time to avoid timezone inconsistencies.

---

### 2. Keeping Code Modular
As features increased (sorting, validation, UI updates), the code became harder to manage. Refactoring into smaller functions helped solve this problem.

---

## How I Improved Through Feedback
Based on improvements made during the contribution phase, I:
- Added sorting functionality for better data exploration
- Introduced validation to handle incorrect inputs safely
- Refactored the code into modular components
- Improved the UI with a card-based layout and summary display

---

## Key Takeaway
The most important lesson from this task is that writing working code is not enough — writing **clean, maintainable, and user-friendly code** is what makes a real-world contribution valuable.

---

## Future Improvements
If I continue this project, I would:
- Connect the app to a live Wikimedia API instead of static JSON
- Add search functionality
- Improve UI styling further using a frontend framework