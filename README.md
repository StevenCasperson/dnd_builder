# D&D Character Builder

[Live Demo](http://127.0.0.1:5000/)  <!-- Replace with your deployed URL if available -->

---

## What is this website?
This is a web-based Dungeons & Dragons 5e character builder. It guides users through the entire process of creating a D&D character, from rolling stats to picking spells, and generates a printable PDF character sheet at the end.

---

## Features & Why They Matter
- **Step-by-step character creation:** Makes the process easy for beginners and thorough for veterans.
- **Interactive forms with validation:** Prevents mistakes and ensures a smooth experience.
- **Custom ability score rolling:** Follows popular house rules for more fun and fairness.
- **Equipment and spell selection with budget tracking:** Keeps choices within game rules and helps new players.
- **Beautiful, medieval-inspired UI:** Immerses users in the fantasy theme.
- **PDF export:** Lets you print or save your finished character for real-life play.

These features were chosen to make character creation accessible, error-free, and enjoyable for all D&D players.

---

## How to Test
- Run `test_dice.py` to verify ability score rolling fairness.
- Run `test_pdf.py` or `tests/test_pdf_smoke.py` to check PDF output.
- To run a test, use:
  ```bash
  python test_dice.py
  python test_pdf.py
  # or
  python tests/test_pdf_smoke.py
  ```

---

## Standard User Flow
1. **Start at the homepage** ([link](http://127.0.0.1:5000/characters/step1))
2. **Roll and assign ability scores**
3. **Choose your race**
4. **Pick your class**
5. **Select skills**
6. **Buy equipment**
7. **Choose spells (if applicable)**
8. **Name your character and review the summary**
9. **Download your character sheet as a PDF**

Each step saves your progress and validates your choices, so you can’t make illegal characters by accident.

---

## Project Structure

```
run.py                  # Main entry point
requirements.txt        # Python dependencies
instance/               # Flask instance folder
static/                 # CSS, images, and static assets
  style.css             # Main app styles
  summary.css           # Character summary sheet styles
  portraits/            # Character portrait images

templates/              # Jinja2 HTML templates
  base.html             # Base layout
  ...                   # Step-by-step and summary templates

dnd_builder/            # Main app package
  __init__.py           # App factory
  characters.py         # Character creation routes
  download.py           # PDF generation
  encounters.py         # (Optional) Encounters logic
  models.py             # Data models
  utils/                # Utility modules (armor, currency, skills, spells)
  data/                 # Data files (equipment, skills, spells)
  forms/                # WTForms classes for each step

tests/                  # Test scripts
  test_pdf_smoke.py     # PDF smoke test
  ...
```

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```bash
   python run.py
   ```
5. **Open in browser:**
   Visit `http://127.0.0.1:5000/`

---

## Testing
- Run `test_dice.py` to verify ability score rolling fairness.
- Run `test_pdf.py` or `tests/test_pdf_smoke.py` to check PDF output.

---

## Customization
- Add new races, classes, equipment, or spells by editing files in `dnd_builder/data/`.
- Update CSS in `static/style.css` and `static/summary.css` for custom themes.
- Portrait images can be added to `static/portraits/` and referenced in templates.

---

## Deployment
- For production, use a WSGI server (e.g., Gunicorn) and set `debug=False` in `run.py`.
- Configure environment variables and secret keys as needed.

---

## Credits
- Built with Flask, Flask-WTF, SQLAlchemy, ReportLab, and Jinja2.
- D&D with Luke Gygax, Ed Greenwood, Alicia Teesh and all the Wisdom she helps provide to the game. (I love her for that.)

---

## License
This project is for educational and personal use. Not affiliated with Wizards of the Coast.
