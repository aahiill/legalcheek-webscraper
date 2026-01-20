# Legal Cheek Web-scraper

A small Python scraper that collects application-deadline information for UK law firm programmes (vacation schemes, insight days, training contracts) from LegalCheek and exports the results to CSV.

## Features
- Find firm pages from the LegalCheek “Most Lists” page
- Visit each firm page and extract programmes listed under the **Deadlines** section
- Capture: programme title, applications open/close dates, and link to the programme
- Export all results to a single CSV file

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies (`requests`, `beautifulsoup4`, `pandas`)

## Install
Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Usage
Run the scraper from the repository root:

```bash
python3 main.py
```

The script writes `legalcheek_deadlines.csv` in the current directory.

## Output
`legalcheek_deadlines.csv` contains the following columns:

- `firm` — firm name
- `title` — programme title
- `applications_open` — opening date (if present)
- `applications_close` — closing date (if present)
- `link` — absolute URL to the programme page