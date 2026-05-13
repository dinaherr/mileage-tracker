[README.md](https://github.com/user-attachments/files/27692841/README.md)
# 📍 Mileage Calculator

A Streamlit web app for calculating point-to-point driving distances using the MapQuest API. Paste addresses directly from Excel, get mileage results instantly, and download a clean report with no addresses included — just the numbers.

---

## Features

- **Paste from Excel** — copy your FROM and TO address columns separately and paste them directly into the app, one address per row
- **Live row preview** — a numbered side-by-side table appears as you paste so you can verify each row matches before calculating
- **Multiple route options** — MapQuest returns up to 3 alternate routes per trip; all are shown in the results table
- **Smart route selection** — the longest route is selected automatically (most conservative mileage), unless it is more than 5 miles above the middle route, in which case the middle route is used as a more realistic number
- **Address shortcuts** — type `PE` instead of the full PE office address; bare street addresses automatically get the default city and state appended
- **Kansas-first state logic** — addresses with no state default to Kansas (KS); if MapQuest finds no match, Missouri (MO) is tried automatically; no other states are ever used
- **Explicit state respected** — if you type KS or MO yourself, that state is used exactly as entered with no fallback
- **Privacy-safe export** — the downloaded CSV and Excel files contain only stop numbers and mileage; no addresses are ever included in the export
- **Light and dark mode** — the UI adapts automatically to your system theme or Streamlit's theme toggle
- **No data stored** — addresses exist only in memory for the current browser session and are never written to disk or logged anywhere

---

## Requirements

```
streamlit
requests
pandas
openpyxl
```

Install all dependencies with:

```bash
pip install streamlit requests pandas openpyxl
```

---

## Setup

### 1. Get a MapQuest API Key

1. Go to [developer.mapquest.com](https://developer.mapquest.com)
2. Create a free account
3. Copy your API key from the dashboard

The free tier includes 15,000 requests per month, which is more than enough for typical use.

### 2. Add Your API Key

Create a file at `.streamlit/secrets.toml` inside your project folder:

```toml
MAPQUEST_API_KEY = "your_api_key_here"
```

> ⚠️ Never commit this file to GitHub or share it. Add `.streamlit/secrets.toml` to your `.gitignore`.

### 3. Project Structure

```
your-project/
├── mileage_calculator.py
└── .streamlit/
    └── secrets.toml
```

### 4. Run the App

```bash
streamlit run mileage_calculator.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## How to Use

### Step 1 — Paste Your FROM Addresses
In Excel, select all cells in your starting-address column, copy (Ctrl+C), click inside the **FROM Addresses** box in the app, and paste (Ctrl+V).

### Step 2 — Paste Your TO Addresses
Do the same for your destination column and paste into the **TO Addresses** box. Each row number must match — row 1 FROM pairs with row 1 TO.

### Step 3 — Verify the Preview
A numbered preview table appears automatically showing both columns side by side. Check that each row looks correct before continuing.

### Step 4 — Click Calculate
The app looks up each route via MapQuest and displays all available route options with the selected mileage highlighted in red.

### Step 5 — Download Results
Use the **Download CSV** or **Download Excel** buttons to export a clean file containing only stop numbers and mileage.

---

## Address Shortcuts & State Rules

| You type | Tool sends to MapQuest | Why |
|---|---|---|
| `PE` | `444 Minnesota Ave, Kansas City, KS 66101` | PE office shorthand |
| `123 Main St` | `123 Main St, Kansas City, KS` — retries as MO if not found | No state → Kansas assumed first, Missouri fallback |
| `456 Elm St, Olathe, KS` | `456 Elm St, Olathe, KS` | Explicit KS → used as-is, no fallback |
| `789 Broadway, Kansas City, MO` | `789 Broadway, Kansas City, MO` | Explicit MO → used as-is, no fallback |
| `Kansas City` | `Kansas City, KS` | City only → KS added automatically |

---

## Route Selection Logic

When MapQuest returns multiple route options:

1. All routes are displayed in the results table (Route 1, Route 2, Route 3)
2. The **longest route** is selected as the most conservative mileage estimate
3. **Outlier check** — if the longest route is more than 5 miles above the middle route, the middle route is used instead as a more realistic number
4. The selected mileage is highlighted in **bold red** in the results table
5. A **Used** column shows exactly which value will be exported
6. All exported mileage is rounded to 1 decimal place (e.g. `12.3`)

---

## Privacy & Data Handling

- Addresses are held **in memory only** for the duration of your browser session
- Closing or refreshing the tab clears all entered data immediately
- **No addresses are ever written to disk**, logged, or persisted between sessions
- The CSV and Excel exports contain **only stop numbers and mileage** — no address data leaves the app through downloads
- MapQuest receives addresses to perform route calculations (required for the lookup), but no data is stored on Streamlit's side
- The API key is stored in `st.secrets` and is never exposed in the UI or logs

---

## Configuration (Sidebar)

All defaults can be adjusted from the sidebar without touching the code:

| Setting | Default | Description |
|---|---|---|
| Default city / state | `Kansas City, KS` | Appended to bare street addresses with no city or state |
| PE shorthand address | `444 Minnesota Ave, Kansas City, KS 66101` | The full address used when `PE` is entered |
| Local area keywords | `Kansas City, KS`, `KS` | Addresses containing these are used exactly as typed |

Changes apply to the current session only and reset when the app restarts.

---

## Troubleshooting

**"API key not found" error**
Make sure `.streamlit/secrets.toml` exists and contains `MAPQUEST_API_KEY = "your_key"` with the correct spelling.

**Route shows as Error**
The address could not be geocoded by MapQuest in either KS or MO. Check for typos, missing street numbers, or ambiguous addresses.

**Row mismatch warning**
The FROM and TO boxes have a different number of non-empty lines. Make sure you copied complete columns from Excel with the same number of rows.

**Only 1 route returned instead of 3**
MapQuest does not always have 3 alternate routes for every trip — short or simple routes may only have 1 or 2 options. This is normal.
