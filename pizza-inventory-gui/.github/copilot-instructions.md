# Copilot Instructions for pizza-inventory-gui

## Project Overview
- This is a Python Tkinter GUI application for pizza inventory and order management.
- Main logic is in `src/five_nights.py` (core classes: `Pizzeria`, `Inventory`, `Order`, `Ingredient`).
- GUI entry point is `src/main.py` (launches Tkinter window, connects buttons to `Pizzeria` methods).
- `src/gui.py` is a minimal/experimental launcher, not the main app.
- Data is managed in-memory; inventory/order logs are saved to text files (`inventory.txt`, `daily_log.txt`, `buy_report.txt`).

## Architecture & Data Flow
- `main.py` creates a `Pizzeria` and `Inventory` instance, then builds the main menu with Tkinter.
- Button callbacks (e.g., `Pizza.Menu`, `Pizza.take_order`) invoke CLI-style workflows from `five_nights.py`.
- All inventory/order logic is in `five_nights.py` (not in the GUI layer).
- No database; persistence is via plain text files.

## Developer Workflows
- **Run app:**
  ```
  cd src
  python main.py
  ```
- **Dependencies:** Install with `pip install -r requirements.txt` (Tkinter is standard in Python).
- **Debugging:** Print statements are used; no logging framework.
- **Testing:** No automated tests present.

## Project Conventions
- All business logic is in `five_nights.py` (avoid duplicating logic in GUI files).
- GUI uses only one geometry manager per window/frame (do not mix `pack` and `grid` in the same parent).
- File paths for icons/assets are absolute in `main.py` (update if moving project).
- All user input validation is handled in `five_nights.py` methods.

## Integration Points
- No external APIs or services.
- Text files (`inventory.txt`, `daily_log.txt`, `buy_report.txt`) are used for persistence/logging.
- Icon file is expected at `src/assets/Pizza -.ico`.

## Examples
- To add an ingredient: use the "Management of Inventory" button, which calls `Pizzeria.Menu()` and then `Inventory.add_ingredient_to_inventory()`.
- To take an order: use the "Take Orders" button, which calls `Pizzeria.take_order()`.

## Key Files
- `src/five_nights.py`: All core logic and data models.
- `src/main.py`: Tkinter GUI entry point.
- `src/assets/`: App icon.
- `README.md`: Basic setup and usage.

---
If any conventions or workflows are unclear, please ask for clarification or provide feedback for improvement.
