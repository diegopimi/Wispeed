# 📡 WiSpeed

> A lightweight web app for monitoring, logging, and visualizing your network's upload and download speeds — on demand or automatically.

---

## Features

- **Instant speed tests** — run a single test with one click
- **Periodic testing** — schedule repeated readings at a custom frequency
- **Timed tests** — queue a reading for a specific time of day
- **Graphical results** — interactive Plotly charts for download & upload trends
- **Reading history** — filterable, sortable log of all recorded sessions
- **Local storage** — all data persisted in a JSON log file, no database required

---

## Setup

### Prerequisites

Install the following before running the project:

```bash
pip install flask speedtest-cli plotly pytest
```

Also install:
- [PlantUML extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml) for VS Code *(for UML diagrams)*
- [Graphviz](https://graphviz.org/download/) *(required by PlantUML)*



---

## ▶️ How to Run

```bash
python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000/
```

> Speed tests take a moment to complete. After clicking **Run Test**, wait a few seconds and refresh the page to see the new reading appear in the table.

---

## Running Tests

From inside the `test/` directory:

```bash
pytest test_app.py > results.txt
```

Results will be saved to `results.txt`.

---

## Roadmap / To-Do

> Items are not listed in priority order.

- The user shall be able to specify the frequency of readings. For example, the user can ask for readings to occur every 25 minutes, every 30 seconds, every day, or any other.
- The user shall be able to specify the time and date in which readings occur. For example February 20th at 5:00 PM and 9:59 PM.
- The app shall keep count of number of readings and reading ID.
- Results shall be presented graphically after every reading, alongside a progress bar or indication of readings left.
- The app shall count with a professional looking user-interface and animations. (Website and app deployment?) 
- Evaluate efficiency and accuracy of test.
- Input validation, no room for crashing.
- Follow consistent coding standards.
- Create UML and following documentation and proper design.
- Comment functionality of the code.
- Users will have the ability to create client accounts / Admin accounts. ( maybe unecessary for the purpose of this app? maybe requires different database? )
- Different layouts (options, website) shall be shown according to user type (client/admin).
- CRUD will be available (preferrably only to admin).
- The project will count with a CI pipeline triggered upon push and PR to ensure the integrity of the builds. 

## 💡 Tips & Tricks

### Editing UML / Sequence Diagrams

1. Right-click the `@startuml` block in VS Code and select **Preview Current Diagram**
2. To export: right-click and choose **Export Current Diagram as SVG**

---

## 📄 License

This project is for personal/educational use. No license applied yet.