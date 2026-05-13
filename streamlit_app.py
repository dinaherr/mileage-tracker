import streamlit as st
import requests
import pandas as pd
import io

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mileage Calculator",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  Styling
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── CSS variables — light mode ── */
:root {
    --bg-page:        #eef1f7;
    --bg-card:        #ffffff;
    --bg-card-alt:    #f4f7fd;
    --bg-input:       #ffffff;
    --border:         #d0d7e8;
    --border-subtle:  #e8ecf5;
    --text-primary:   #0d1b38;
    --text-secondary: #4a5878;
    --text-muted:     #7b8caa;
    --accent:         #1a4fd6;
    --accent-hover:   #1340b0;
    --accent-light:   #dde8ff;
    --header-bg:      #0d1b38;
    --header-text:    #ffffff;
    --header-sub:     #7b9fd4;
    --step-bg:        #1a4fd6;
    --step-text:      #ffffff;
    --step-label:     #0d1b38;
    --metric-bg:      #ffffff;
    --metric-num:     #0d1b38;
    --metric-accent:  #1a4fd6;
    --metric-lbl:     #4a5878;
    --warn-bg:        #fff8e6;
    --warn-border:    #f59e0b;
    --warn-text:      #7a4500;
    --info-bg:        #e8f0ff;
    --info-border:    #1a4fd6;
    --info-text:      #0d2d8a;
    --how-bg:         #f4f7fd;
    --how-border:     #d0d7e8;
    --how-text:       #1e2d50;
    --table-th-bg:    #e8edf8;
    --table-th-text:  #1e2d50;
    --table-border:   #d0d7e8;
    --sidebar-bg:     #f4f7fd;
    --sidebar-border: #d0d7e8;
}

/* ── CSS variables — dark mode ── */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-page:        #0d1117;
        --bg-card:        #161c2d;
        --bg-card-alt:    #1c2440;
        --bg-input:       #1c2440;
        --border:         #2e3d5e;
        --border-subtle:  #243050;
        --text-primary:   #e8edf8;
        --text-secondary: #9aaecf;
        --text-muted:     #5d7099;
        --accent:         #4f85ff;
        --accent-hover:   #6b99ff;
        --accent-light:   #1a2d5a;
        --header-bg:      #0a1628;
        --header-text:    #ffffff;
        --header-sub:     #6b99cc;
        --step-bg:        #4f85ff;
        --step-text:      #ffffff;
        --step-label:     #c8d8f8;
        --metric-bg:      #161c2d;
        --metric-num:     #e8edf8;
        --metric-accent:  #4f85ff;
        --metric-lbl:     #7b9ac8;
        --warn-bg:        #2a1f00;
        --warn-border:    #f59e0b;
        --warn-text:      #fcd47a;
        --info-bg:        #0e1f45;
        --info-border:    #4f85ff;
        --info-text:      #93b8ff;
        --how-bg:         #161c2d;
        --how-border:     #2e3d5e;
        --how-text:       #c8d8f8;
        --table-th-bg:    #1c2440;
        --table-th-text:  #c8d8f8;
        --table-border:   #2e3d5e;
        --sidebar-bg:     #111827;
        --sidebar-border: #1f2d4a;
    }
}

/* Streamlit dark mode override — Streamlit sets [data-theme="dark"] on <body> */
[data-theme="dark"] {
    --bg-page:        #0d1117;
    --bg-card:        #161c2d;
    --bg-card-alt:    #1c2440;
    --bg-input:       #1c2440;
    --border:         #2e3d5e;
    --border-subtle:  #243050;
    --text-primary:   #e8edf8;
    --text-secondary: #9aaecf;
    --text-muted:     #5d7099;
    --accent:         #4f85ff;
    --accent-hover:   #6b99ff;
    --accent-light:   #1a2d5a;
    --header-bg:      #0a1628;
    --header-text:    #ffffff;
    --header-sub:     #6b99cc;
    --step-bg:        #4f85ff;
    --step-text:      #ffffff;
    --step-label:     #c8d8f8;
    --metric-bg:      #161c2d;
    --metric-num:     #e8edf8;
    --metric-accent:  #4f85ff;
    --metric-lbl:     #7b9ac8;
    --warn-bg:        #2a1f00;
    --warn-border:    #f59e0b;
    --warn-text:      #fcd47a;
    --info-bg:        #0e1f45;
    --info-border:    #4f85ff;
    --info-text:      #93b8ff;
    --how-bg:         #161c2d;
    --how-border:     #2e3d5e;
    --how-text:       #c8d8f8;
    --table-th-bg:    #1c2440;
    --table-th-text:  #c8d8f8;
    --table-border:   #2e3d5e;
    --sidebar-bg:     #111827;
    --sidebar-border: #1f2d4a;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp { background: var(--bg-page) !important; }
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1060px;
}

/* ── Header ── */
.app-header {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    background: var(--header-bg);
    border-radius: 12px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.8rem;
    border: 1px solid rgba(255,255,255,0.07);
}
.app-header-text h1 {
    margin: 0;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--header-text);
    letter-spacing: -0.4px;
}
.app-header-text p {
    margin: 0.3rem 0 0;
    font-size: 0.9rem;
    color: var(--header-sub);
}

/* ── Section cards ── */
.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.6rem 1.9rem 2rem;
    margin-bottom: 1.4rem;
}

/* ── Step label — bigger, bolder, dark-blue ── */
.section-label {
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0;
    text-transform: none;
    color: var(--step-label);
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

/* ── Step badge ── */
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px; height: 30px;
    background: var(--step-bg);
    color: var(--step-text);
    border-radius: 50%;
    font-size: 0.9rem;
    font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(26,79,214,0.3);
}

/* ── How-to instruction box ── */
.how-to {
    background: var(--how-bg);
    border: 1px solid var(--how-border);
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    font-size: 0.88rem;
    color: var(--how-text);
    line-height: 1.7;
    margin-bottom: 0.2rem;
}
.how-to strong { color: var(--accent); }
.shorthand-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.84rem;
    margin-top: 0.6rem;
}
.shorthand-table th {
    background: var(--table-th-bg);
    color: var(--table-th-text);
    font-weight: 700;
    padding: 0.5rem 0.9rem;
    text-align: left;
    border-bottom: 2px solid var(--table-border);
}
.shorthand-table td {
    padding: 0.45rem 0.9rem;
    border-bottom: 1px solid var(--border-subtle);
    color: var(--how-text);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
}
.shorthand-table tr:last-child td { border-bottom: none; }

/* ── Metric cards ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.4rem;
}
.metric-card {
    background: var(--metric-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem 1.3rem;
    text-align: center;
    border-top: 3px solid var(--accent);
}
.metric-num {
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--metric-num);
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1.1;
}
.metric-num.accent { color: var(--metric-accent); }
.metric-lbl {
    font-size: 0.8rem;
    color: var(--metric-lbl);
    margin-top: 0.35rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.97rem !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 2px 10px rgba(26,79,214,0.25) !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: var(--accent-hover) !important; }
.stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

/* ── Textareas ── */
.stTextArea label {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    font-size: 0.92rem !important;
}
.stTextArea textarea {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    background: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border-color: var(--border) !important;
}

/* ── Alerts ── */
.alert-warn {
    background: var(--warn-bg);
    border-left: 4px solid var(--warn-border);
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1.2rem;
    font-size: 0.9rem;
    color: var(--warn-text);
    margin-bottom: 1rem;
    font-weight: 500;
}
.alert-info {
    background: var(--info-bg);
    border-left: 4px solid var(--info-border);
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1.2rem;
    font-size: 0.9rem;
    color: var(--info-text);
    margin-bottom: 1rem;
    font-weight: 500;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--sidebar-border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── General text readability ── */
p, li, span, label, div {
    color: var(--text-primary);
}
small { color: var(--text-secondary) !important; }
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
DEFAULT_CITY_STATE = "Kansas City, KS"
PE_ADDRESS         = "444 Minnesota Ave, Kansas City, KS 66101"
LOCAL_KEYWORDS     = ["Kansas City", "KS", "MO"]

# ─────────────────────────────────────────────
#  Sidebar — configuration
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.caption("Adjust defaults here without changing any code.")

    default_city = st.text_input(
        "Default city / state",
        value=DEFAULT_CITY_STATE,
        help="Automatically appended to any address that has no city or state.",
    )
    pe_address = st.text_input(
        "PE shorthand address",
        value=PE_ADDRESS,
        help="When 'PE' is entered as an address, this full address is used.",
    )

    st.markdown("---")
    st.markdown("**Local area keywords**")
    st.caption(
        "Addresses containing any of these words are used exactly as typed "
        "(no default city added)."
    )
    local_kw_str = st.text_area(
        "Keywords (one per line)",
        value="\n".join(LOCAL_KEYWORDS),
        height=140,
        label_visibility="collapsed",
    )
    local_keywords = [k.strip() for k in local_kw_str.split("\n") if k.strip()]

    st.markdown("---")
    st.caption("🔑 API key loaded from `st.secrets['MAPQUEST_API_KEY']`")

# ─────────────────────────────────────────────
#  Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div style="font-size:2.2rem">📍</div>
  <div class="app-header-text">
    <h1>Mileage Calculator</h1>
    <p>Paste addresses from your Excel spreadsheet · calculate distances · download results</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Step 1 — Instructions
# ─────────────────────────────────────────────
with st.expander("📋  How to use — click to expand", expanded=True):
    st.markdown("""
<div class="how-to">
<strong>Step 1 &nbsp;·&nbsp; Copy your FROM column in Excel</strong><br>
Click the top of your starting-address column, select all cells, copy (Ctrl+C),
then click inside the <em>FROM Addresses</em> box below and paste (Ctrl+V).<br><br>

<strong>Step 2 &nbsp;·&nbsp; Copy your TO column in Excel</strong><br>
Do the same for your destination column and paste into the <em>TO Addresses</em> box.
Each row number must match — row 1 FROM goes to row 1 TO, and so on.<br><br>

<strong>Step 3 &nbsp;·&nbsp; Click Calculate</strong><br>
Distances are looked up automatically. When done, download your results as CSV or Excel.<br><br>

<strong>Address shortcuts you can use:</strong>
<table class="shorthand-table">
  <thead><tr><th>You type</th><th>Tool uses</th><th>Why</th></tr></thead>
  <tbody>
    <tr>
      <td>PE</td>
      <td>444 Minnesota Ave, Kansas City, KS 66101</td>
      <td>PE office shorthand</td>
    </tr>
    <tr>
      <td>123 Main St</td>
      <td>123 Main St, Kansas City, KS</td>
      <td>No city → default city added</td>
    </tr>
    <tr>
      <td>456 Elm St, Olathe, KS</td>
      <td>456 Elm St, Olathe, KS</td>
      <td>Already has city/state → used as-is</td>
    </tr>
  </tbody>
</table>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Step 2 — Paste addresses
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <div class="section-label">
    <span class="step-badge">1</span>&nbsp; Paste Your Addresses
  </div>
""", unsafe_allow_html=True)

col_from, col_to = st.columns(2, gap="medium")

with col_from:
    st.markdown(
        "**FROM — Starting addresses**\n\n"
        "<small style=\'color:#6b7280\'>Copy your starting-address column from Excel and paste here — one address per row</small>",
        unsafe_allow_html=True,
    )
    from_raw = st.text_area(
        "from_addresses",
        height=230,
        placeholder="123 Main St\nPE\n789 Oak Ave, Overland Park, KS\n321 Broadway",
        label_visibility="collapsed",
    )

with col_to:
    st.markdown(
        "**TO — Destination addresses**\n\n"
        "<small style=\'color:#6b7280\'>Copy your destination column from Excel and paste here — one address per row</small>",
        unsafe_allow_html=True,
    )
    to_raw = st.text_area(
        "to_addresses",
        height=230,
        placeholder="456 Elm St\n321 Broadway\n555 Pine Rd\n100 State Ave",
        label_visibility="collapsed",
    )

st.markdown("</div>", unsafe_allow_html=True)

# Live row-count feedback + numbered preview table
from_lines = [l for l in from_raw.strip().split("\n") if l.strip()]
to_lines   = [l for l in to_raw.strip().split("\n") if l.strip()]

if from_lines or to_lines:
    if len(from_lines) == len(to_lines) and from_lines:
        st.markdown(
            f'<div class="alert-info">✅ &nbsp;<strong>{len(from_lines)}</strong> FROM '
            f'and <strong>{len(to_lines)}</strong> TO addresses — counts match, ready to calculate!</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="alert-warn">⚠️ &nbsp;<strong>{len(from_lines)}</strong> FROM '
            f'and <strong>{len(to_lines)}</strong> TO addresses — '
            f'counts must match before calculating.</div>',
            unsafe_allow_html=True,
        )

    # Numbered side-by-side preview — helps her verify rows match Excel
    max_preview = max(len(from_lines), len(to_lines))
    preview_rows = []
    for i in range(max_preview):
        preview_rows.append({
            "Row": i + 1,
            "FROM Address": from_lines[i] if i < len(from_lines) else "—",
            "TO Address":   to_lines[i]   if i < len(to_lines)   else "—",
        })
    import pandas as _pd_prev
    preview_df = _pd_prev.DataFrame(preview_rows)

    def _stripe_preview(row):
        base = "background-color: #f9fafc" if row.name % 2 == 0 else "background-color: #ffffff"
        return [base] * len(row)

    styled_preview = preview_df.style.apply(_stripe_preview, axis=1).set_properties(
        subset=["Row"], **{"text-align": "center", "color": "#9ca3af", "width": "40px"}
    )
    with st.expander("🔍  Preview — verify your rows match before calculating", expanded=(max_preview > 0)):
        st.dataframe(styled_preview, use_container_width=True, hide_index=True, height=min(36 * max_preview + 40, 320))

# ─────────────────────────────────────────────
#  Calculate button
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label" style="margin-top:0.4rem">
  <span class="step-badge">2</span>&nbsp; Calculate
</div>
""", unsafe_allow_html=True)

go = st.button("📍  Calculate Mileage", use_container_width=False)

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def format_address(raw: str, kw_list: list, default_cs: str, pe_addr: str) -> str:
    line = raw.strip()
    if line.upper() == "PE":
        return pe_addr
    if any(kw in line for kw in kw_list):
        return line
    return f"{line}, {default_cs}"

def get_all_routes(from_addr: str, to_addr: str, api_key: str):
    """
    Fetch up to 3 alternate routes from MapQuest and return a list of
    distances (miles), sorted shortest first.  Returns [] on failure.
    """
    try:
        resp = requests.get(
            "http://www.mapquestapi.com/directions/v2/alternateroutes",
            params={
                "key":         api_key,
                "from":        from_addr,
                "to":          to_addr,
                "unit":        "m",
                "maxRoutes":   3,
            },
            timeout=15,
        )
        data = resp.json()
        if resp.status_code != 200 or data["info"]["statuscode"] != 0:
            return []

        distances = []
        # Primary route
        if "route" in data and "distance" in data["route"]:
            distances.append(round(data["route"]["distance"], 2))
        # Alternate routes
        for alt in data.get("alternateRoutes", []):
            route = alt.get("route", {})
            if "distance" in route:
                distances.append(round(route["distance"], 2))

        return sorted(distances, reverse=True)   # longest first
    except Exception:
        return []

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Mileage Results")
        ws = writer.sheets["Mileage Results"]
        for col in ws.columns:
            width = max(len(str(c.value or "")) for c in col) + 4
            ws.column_dimensions[col[0].column_letter].width = min(width, 65)
    return buf.getvalue()

# ─────────────────────────────────────────────
#  Run calculation
# ─────────────────────────────────────────────
if go:
    try:
        API_KEY = st.secrets["MAPQUEST_API_KEY"]
    except Exception:
        st.markdown(
            '<div class="alert-warn">⚠️ <strong>API key not found.</strong> '
            'Add <code>MAPQUEST_API_KEY</code> to your <code>.streamlit/secrets.toml</code>.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    if not from_lines or not to_lines:
        st.markdown(
            '<div class="alert-warn">⚠️ Please paste addresses into both boxes before calculating.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    if len(from_lines) != len(to_lines):
        st.markdown(
            f'<div class="alert-warn">⚠️ <strong>Row mismatch.</strong> '
            f'FROM has {len(from_lines)} rows, TO has {len(to_lines)} rows. '
            f'Make sure you copied full columns with the same number of addresses.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    from_addrs = [format_address(l, local_keywords, default_city, pe_address) for l in from_lines]
    to_addrs   = [format_address(l, local_keywords, default_city, pe_address) for l in to_lines]

    rows = []
    bar  = st.progress(0, text="Looking up route 1…")
    for i, (fa, ta) in enumerate(zip(from_addrs, to_addrs)):
        bar.progress((i + 1) / len(from_addrs), text=f"Looking up route {i + 1} of {len(from_addrs)}…")
        all_distances = get_all_routes(fa, ta, API_KEY)
        # Pick mileage to export:
        # Use the longest route, UNLESS it is >5 mi more than the middle route
        # (outlier check) — in that case use the middle route instead.
        if all_distances:
            longest = all_distances[0]  # list is sorted longest-first
            if len(all_distances) >= 3:
                middle = all_distances[1]
                chosen = middle if (longest - middle) > 5 else longest
            else:
                chosen = longest
        else:
            chosen = None

        rows.append({
            "stop":      i + 1,
            "from_raw":  from_lines[i].strip(),
            "from":      fa,
            "to_raw":    to_lines[i].strip(),
            "to":        ta,
            "routes":    all_distances,   # sorted longest first
            "best":      chosen,
            "ok":        len(all_distances) > 0,
        })
    bar.empty()

    numeric  = [r["best"] for r in rows if r["ok"]]
    total_mi = round(sum(numeric), 1) if numeric else 0
    avg_mi   = round(total_mi / len(numeric), 1) if numeric else 0
    errors   = sum(1 for r in rows if not r["ok"])

    # Metrics
    st.markdown(f"""
    <div class="metrics-row">
      <div class="metric-card">
        <div class="metric-num accent">{total_mi}</div>
        <div class="metric-lbl">Total Miles</div>
      </div>
      <div class="metric-card">
        <div class="metric-num">{len(rows)}</div>
        <div class="metric-lbl">Routes Calculated</div>
      </div>
      <div class="metric-card">
        <div class="metric-num">{avg_mi}</div>
        <div class="metric-lbl">Avg Miles / Route</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if errors:
        st.markdown(
            f'<div class="alert-warn">⚠️ <strong>{errors} route{"s" if errors > 1 else ""} '
            f'could not be calculated.</strong> Check that those addresses are complete and correctly spelled.</div>',
            unsafe_allow_html=True,
        )

    # Results table — one row per stop, one column per route option
    st.markdown("""
    <div class="section-card">
      <div class="section-label"><span class="step-badge">3</span>&nbsp; Results</div>
    """, unsafe_allow_html=True)

    # Build display dataframe — pad route columns so all rows have same width
    # Routes are sorted longest-first; round all to 1 decimal for display
    max_routes = max((len(r["routes"]) for r in rows), default=1)
    route_col_names = [f"Route {i+1} (mi)" for i in range(max_routes)]

    display_rows = []
    for r in rows:
        row = {
            "#":     r["stop"],
            "From":  r["from"],
            "To":    r["to"],
        }
        for i, col in enumerate(route_col_names):
            val = r["routes"][i] if i < len(r["routes"]) else None
            row[col] = round(val, 1) if val is not None else None
        row["Used"] = round(r["best"], 1) if r["best"] is not None else "Error"
        row["Status"] = "✓ OK" if r["ok"] else "✗ Error"
        display_rows.append(row)

    display_df = pd.DataFrame(display_rows)

    # Bold red text on whichever route column matches the chosen mileage.
    # "Used" column stays plain black. No background fill anywhere.
    def highlight_chosen(row_s):
        styles = [""] * len(row_s)
        best_val = row_s.get("Used")
        if best_val == "Error" or best_val is None:
            return styles
        for col in route_col_names:
            if col in row_s.index and row_s[col] == best_val:
                idx = list(row_s.index).index(col)
                styles[idx] = "color: #991b1b; font-weight: 700"
        return styles

    # Format all numeric columns to exactly 1 decimal place (5.9 not 5.90000)
    def _fmt_mi(v):
        if v is None or (isinstance(v, float) and v != v):
            return "—"
        try:
            return f"{float(v):.1f}"
        except Exception:
            return str(v)

    format_dict = {col: _fmt_mi for col in route_col_names}
    format_dict["Used"] = _fmt_mi

    styled = (
        display_df.style
        .apply(highlight_chosen, axis=1)
        .format(format_dict, na_rep="—")
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.caption(
        f"🔴 Highlighted = mileage used in export (longest route, or middle if longest is 5+ mi above middle)   ·   "
        f"Total: {total_mi} mi   ·   "
        f"Addresses shown for verification only — not included in any download."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Downloads — export chosen mileage only (rounded to 1 decimal), no addresses
    st.markdown("""
    <div class="section-card">
      <div class="section-label"><span class="step-badge">4</span>&nbsp; Download Results</div>
    """, unsafe_allow_html=True)

    export_rows = [{
        "Stop #": r["stop"],
        "Miles": round(r["best"], 1) if r["ok"] else "Error",
    } for r in rows]
    export_rows.append({"Stop #": "TOTAL", "Miles": total_mi})
    export_df = pd.DataFrame(export_rows)

    dl1, dl2, spacer = st.columns([1, 1, 3])
    with dl1:
        st.download_button(
            "⬇️  Download CSV",
            data=export_df.to_csv(index=False).encode(),
            file_name="mileage_results.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            "⬇️  Download Excel",
            data=to_excel_bytes(export_df),
            file_name="mileage_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
