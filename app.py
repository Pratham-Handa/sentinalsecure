import streamlit as st
import pandas as pd
import numpy as np
import joblib
from streamlit.components.v1 import html

# =========================
# 0. UI BEAUTIFICATION LAYER
# (No logic changes, just CSS/HTML injection)
# =========================

def setup_interface():
    # Global cyberpunk theme using CSS + some structural HTML helpers
    st.markdown(
        """
    <style>
        /* ================================
           GLOBAL / ROOT
        ==================================*/
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;600&display=swap');

        :root {
            --bg-main: #05060a;
            --bg-elevated: #101320;
            --bg-elevated-soft: #14172a;
            --accent-primary: #00f3ff;
            --accent-secondary: #ff00c8;
            --accent-danger: #ff004c;
            --text-main: #e4ecff;
            --text-muted: #7f8ca8;
            --border-subtle: #262a3c;
            --shadow-soft: 0 18px 45px rgba(0, 0, 0, 0.6);
            --radius-card: 14px;
        }

        .stApp {
            background: radial-gradient(circle at 0 0, #1a1038 0, #05060a 55%) fixed;
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        /* Soft glow background grid */
        .cyber-grid::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(0, 243, 255, 0.06) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 0, 200, 0.06) 1px, transparent 1px);
            background-size: 40px 40px;
            opacity: 0.6;
            pointer-events: none;
            z-index: -1;
        }

        /* ================================
           HEADERS / TITLES
        ==================================*/
        h1, h2, h3 {
            font-family: 'Fira Code', monospace;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        h1 {
            color: #ffffff;
            font-size: 1.9rem;
            margin-bottom: 0.4rem;
        }

        .app-subtitle {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            color: var(--text-muted);
        }

        .neon-divider {
            height: 2px;
            width: 100%;
            margin: 14px 0 20px;
            position: relative;
            background: linear-gradient(90deg,
                rgba(0, 243, 255, 0) 0%,
                rgba(0, 243, 255, 0.7) 30%,
                rgba(255, 0, 200, 0.7) 70%,
                rgba(255, 0, 200, 0) 100%);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.35);
        }

        .neon-divider::after {
            content: "SENTINEL·SECURE CORE";
            position: absolute;
            top: -12px;
            right: 0;
            font-family: 'Fira Code', monospace;
            font-size: 0.6rem;
            padding: 2px 10px;
            border-radius: 999px;
            background: radial-gradient(circle at 0 0, rgba(0,243,255,0.2), rgba(10,11,16,0.95));
            border: 1px solid rgba(0,243,255,0.4);
            color: var(--text-muted);
        }

        /* Tagline chip row */
        .status-banner {
            display: inline-flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            padding: 10px 12px;
            background: radial-gradient(circle at 0 0, rgba(255,0,76,0.14), rgba(10,11,18,0.96));
            border-radius: 999px;
            border: 1px solid rgba(255, 0, 76, 0.5);
            box-shadow: 0 0 18px rgba(255, 0, 76, 0.23);
            font-size: 0.7rem;
        }

        .status-chip {
            padding: 3px 10px;
            border-radius: 999px;
            border: 1px solid rgba(100, 255, 218, 0.4);
            background: rgba(15, 23, 42, 0.8);
            color: var(--text-muted);
            font-family: 'Fira Code', monospace;
        }

        .status-chip strong {
            color: var(--accent-primary);
        }

        .status-danger {
            color: var(--accent-danger);
        }

        /* ================================
           SIDEBAR - CYBERPUNK NAV
        ==================================*/
        [data-testid="stSidebar"] {
            background: radial-gradient(circle at 0 0, #1b1038 0, #05060a 60%);
            border-right: 1px solid var(--border-subtle);
            box-shadow: 15px 0 40px rgba(0, 0, 0, 0.9);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem;
        }

        .side-title {
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: var(--accent-primary);
            margin-bottom: 0.5rem;
        }

        .side-subtitle {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--text-muted);
            margin-bottom: 1.2rem;
        }

        .side-logo-tag {
            font-size: 0.6rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            padding: 3px 9px;
            border-radius: 999px;
            border: 1px solid rgba(0,243,255,0.55);
            color: var(--accent-primary);
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin-bottom: 0.9rem;
        }

        .side-logo-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--accent-primary);
            box-shadow: 0 0 10px rgba(0,243,255,0.9);
        }

        /* Streamlit radio nav transformed into cyberpunk nav-pills */
        .stRadio > label {
            display: none !important;
        }

        .stRadio > div {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }

        .stRadio [role="radio"] {
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.35);
            padding: 0.55rem 0.7rem;
            position: relative;
            cursor: pointer;
            background: linear-gradient(135deg,
                rgba(15,23,42,0.96),
                rgba(17,24,39,0.96));
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.75);
            transition: all 0.18s ease-out;
            font-size: 0.8rem;
        }

        .stRadio [role="radio"]:hover {
            border-color: rgba(0,243,255,0.7);
            box-shadow: 0 0 18px rgba(0,243,255,0.28);
            transform: translateY(-1px);
        }

        .stRadio [role="radio"][aria-checked="true"] {
            border-color: rgba(255,0,200,0.8);
            background:
                linear-gradient(120deg,
                    rgba(0,243,255,0.18),
                    rgba(255,0,200,0.15)),
                radial-gradient(circle at 0 0, rgba(0,243,255,0.17), rgba(10,10,15,0.95));
            box-shadow:
                0 0 22px rgba(0,243,255,0.45),
                0 0 36px rgba(255,0,200,0.4);
        }

        .stRadio [role="radio"]::before {
            content: "";
            position: absolute;
            left: 8px;
            top: 50%;
            transform: translateY(-50%);
            width: 8px;
            height: 8px;
            border-radius: 50%;
            border: 1px solid rgba(148,163,184,0.6);
            box-shadow: 0 0 6px rgba(148,163,184,0.5);
        }

        .stRadio [role="radio"][aria-checked="true"]::before {
            border-color: rgba(0,243,255,0.9);
            background: var(--accent-primary);
            box-shadow: 0 0 12px rgba(0,243,255,0.9);
        }

        .stRadio [role="radio"] p {
            margin-left: 16px;
            font-family: 'Fira Code', monospace;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .side-info-box {
            margin-top: 1.4rem;
            padding: 0.9rem 0.8rem;
            border-radius: var(--radius-card);
            background: linear-gradient(145deg,
                rgba(15,23,42,0.98),
                rgba(2,6,23,0.98));
            border: 1px dashed rgba(148, 163, 184, 0.35);
            font-size: 0.7rem;
            color: var(--text-muted);
            box-shadow: 0 12px 30px rgba(0,0,0,0.75);
        }

        .side-info-box strong {
            color: var(--accent-primary);
        }

        /* ================================
           CARDS / METRICS / BUTTONS
        ==================================*/
        .cyber-card {
            background: linear-gradient(135deg,
                rgba(15,23,42,0.98),
                rgba(2,6,23,0.98));
            border-radius: var(--radius-card);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-soft);
            padding: 18px 20px;
            position: relative;
            overflow: hidden;
        }

        .cyber-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 0 0,
                rgba(0,243,255,0.15),
                transparent 55%);
            opacity: 0.7;
            pointer-events: none;
        }

        .cyber-card::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: inherit;
            border: 1px solid rgba(0,243,255,0.12);
            mix-blend-mode: screen;
            pointer-events: none;
        }

        div[data-testid="stMetric"] {
            background: radial-gradient(circle at 0 0,
                rgba(0,243,255,0.12),
                rgba(15,23,42,0.98));
            border-radius: var(--radius-card);
            border: 1px solid rgba(37, 99, 235, 0.45);
            box-shadow: 0 16px 36px rgba(15,23,42,0.95);
            padding: 12px 14px;
            position: relative;
            overflow: hidden;
        }

        div[data-testid="stMetricLabel"] {
            color: var(--text-muted);
            font-size: 0.8rem;
            font-family: 'Fira Code', monospace;
        }

        div[data-testid="stMetricValue"] {
            color: #f9fafb;
            font-family: 'Fira Code', monospace;
            font-weight: 600;
            font-size: 1.1rem;
        }

        .stButton > button {
            background:
                linear-gradient(120deg,
                    rgba(0,243,255,0.16),
                    rgba(255,0,200,0.18));
            color: #e5e7eb;
            border-radius: 999px;
            border: 1px solid rgba(0,243,255,0.7);
            font-family: 'Fira Code', monospace;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.7rem;
            padding: 0.55rem 0.4rem;
            box-shadow:
                0 10px 30px rgba(15,23,42,0.9),
                0 0 22px rgba(0,243,255,0.27);
            transition: all 0.16s ease-out;
        }

        .stButton > button:hover {
            background:
                linear-gradient(120deg,
                    rgba(0,243,255,0.32),
                    rgba(255,0,200,0.33));
            color: #0b1120;
            box-shadow:
                0 0 18px rgba(0,243,255,0.55),
                0 0 35px rgba(255,0,200,0.55);
            transform: translateY(-1px);
        }

        [data-testid="stDataFrame"] {
            border-radius: var(--radius-card);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-soft);
            overflow: hidden;
        }

        .stJson {
            background: #020617;
            border-radius: var(--radius-card);
            border: 1px solid rgba(15, 23, 42, 0.8);
            padding: 0.8rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.78rem;
            box-shadow: 0 12px 32px rgba(0,0,0,0.8);
        }

        code, pre {
            font-family: 'Fira Code', monospace !important;
            font-size: 0.78rem;
        }

        .stAlert {
            background: radial-gradient(circle at 0 0,
                rgba(0,243,255,0.25),
                rgba(15,23,42,0.98));
            border-radius: var(--radius-card);
            border: 1px solid rgba(0,243,255,0.65);
            box-shadow: 0 0 30px rgba(0,243,255,0.3);
        }

        /* ===== Threat feed ===== */
        .threat-feed-container {
            margin-top: 0.5rem;
            margin-bottom: 0.9rem;
            border-radius: 14px;
            border: 1px solid rgba(248,113,113,0.75);
            background: linear-gradient(135deg,
                rgba(15,23,42,0.96),
                rgba(24,24,27,0.98));
            box-shadow: 0 18px 40px rgba(0,0,0,0.9);
            padding: 8px 10px 10px;
            position: relative;
            overflow: hidden;
        }

        .threat-feed-container::before {
            content: "LIVE THREAT FEED";
            position: absolute;
            top: 4px;
            left: 10px;
            font-family: 'Fira Code', monospace;
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: rgba(248,250,252,0.7);
        }

        .threat-feed {
            margin-top: 18px;
            max-height: 210px;
            overflow-y: auto;
            padding-right: 4px;
        }

        .threat-feed-container::after {
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 18px;
            background: linear-gradient(to top,
                rgba(15,23,42,1),
                rgba(15,23,42,0));
            pointer-events: none;
        }

        .threat-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.75rem;
            font-family: 'Fira Code', monospace;
        }

        .threat-table thead {
            position: sticky;
            top: 0;
            background: rgba(15,23,42,0.98);
            z-index: 1;
        }

        .threat-table th,
        .threat-table td {
            padding: 4px 8px;
            border-bottom: 1px solid rgba(55,65,81,0.7);
            white-space: nowrap;
        }

        .threat-table th {
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.7rem;
            color: rgba(209,213,219,0.9);
        }

        .threat-table tbody tr {
            transition: background 0.15s ease-out, transform 0.15s ease-out;
        }

        .threat-table tbody tr:hover {
            background: rgba(127,29,29,0.8);
            transform: translateX(2px);
        }

        .threat-table tbody tr td:first-child {
            color: #f97373;
        }

        /* Blinking intrusion indicator */
        .intrusion-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid rgba(248,113,113,0.95);
            background: radial-gradient(circle at 0 0,
                rgba(239,68,68,0.35),
                rgba(15,23,42,0.98));
            font-family: 'Fira Code', monospace;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: rgba(254,242,242,0.95);
            margin-bottom: 0.4rem;
            box-shadow:
                0 0 18px rgba(239,68,68,0.8),
                0 10px 30px rgba(0,0,0,0.9);
        }

        .intrusion-indicator-dot {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            background: #f97373;
            box-shadow: 0 0 18px rgba(239,68,68,1);
            animation: blinkDot 1s infinite alternate;
        }

        @keyframes blinkDot {
            0%   { opacity: 1; transform: scale(1); }
            100% { opacity: 0.3; transform: scale(1.35); }
        }

        /* Neon loader */
        .neon-loader {
            width: 100%;
            height: 4px;
            border-radius: 999px;
            background: rgba(15,23,42,0.95);
            border: 1px solid rgba(148,163,184,0.6);
            overflow: hidden;
            box-shadow: 0 0 18px rgba(0,0,0,0.9);
            margin: 8px 0 6px;
        }

        .neon-loader-bar {
            width: 40%;
            height: 100%;
            background: linear-gradient(90deg,
                rgba(0,243,255,0),
                rgba(0,243,255,1),
                rgba(255,0,200,0));
            animation: slideLoader 1.2s linear infinite;
        }

        @keyframes slideLoader {
            0%   { transform: translateX(-60%); }
            100% { transform: translateX(150%); }
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #020617;
        }
        ::-webkit-scrollbar-thumb {
            background: #272b3c;
            border-radius: 999px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-primary);
        }

    </style>
    """,
        unsafe_allow_html=True,
    )

    # Background grid element
    st.markdown('<div class="cyber-grid"></div>', unsafe_allow_html=True)


# =========================
# BASIC PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SentinelSecure 0.1 - Intrusion Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Call the UI setup immediately after page config
setup_interface()

# ----- NEW: import explainability helpers -----
try:
    from explain import explain_flow, simple_explanation, load_error
except Exception as e:
    explain_flow = None
    simple_explanation = None
    load_error = f"Could not import explain_flow/simple_explanation from explain.py: {e}"

# ----- NEW: import threat ledger helpers -----
try:
    from ledger import add_log, verify_chain, get_chain_as_list
except Exception:
    add_log = None
    verify_chain = None
    get_chain_as_list = None

# =========================
# AUTH GATE (LIGHTWEIGHT)
# =========================

def auth_gate():
    # Initialise auth state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "auth_success" not in st.session_state:
        st.session_state["auth_success"] = False

    # If already authenticated → skip gate entirely
    if st.session_state["authenticated"]:
        return

    st.markdown("### 🔐 SentinelSecure Access Gate")
    st.caption("Restricted SOC console. Enter the access code to proceed.")

    # 🔑 Change this if needed
    CORRECT_CODE = "sentinel-sec-24"

    access_code = st.text_input("Access Code", type="password")

    if st.button("Enter Console"):
        if access_code == CORRECT_CODE:
            st.session_state["authenticated"] = True
            st.session_state["auth_success"] = True  # flag for next run
            # clean refresh so UI fully switches
            try:
                st.rerun()
            except Exception:
                try:
                    st.experimental_rerun()
                except Exception:
                    pass
        else:
            st.toast("🚫 Incorrect code — Access denied.", icon="❌")

    # Still not authenticated → block rest of the app
    if not st.session_state["authenticated"]:
        st.stop()




# =========================
# TITLE SECTION (BEAUTIFIED)
# =========================

col_logo, col_title = st.columns([1, 6])
with col_title:
    st.markdown("""
        <div>
            <div class="app-subtitle">NEURAL INTRUSION DEFENCE LAYER</div>
        </div>
    """, unsafe_allow_html=True)
    st.title("🛡️ SentinelSecure // PROTOTYPE")

    st.markdown("""
        <div class="status-banner">
            <span class="status-chip"><span class="status-danger">●</span> STATUS: <strong>ACTIVE</strong></span>
            <span class="status-chip">SYSTEM: IDS · DEEP INSPECTION CORE</span>
            <span class="status-chip">MODULES: BULK ANALYSIS · PLAYGROUND · WHAT-IF SIM</span>
        </div>
        <div class="neon-divider"></div>
    """, unsafe_allow_html=True)

# =========================
# 1. LOAD THE TRAINED MODEL
# =========================

@st.cache_resource
def load_model():
    """
    Loads the trained model from best_threshold.pkl.
    Assumes this file is in the SAME FOLDER as this app.py.
    """
    model_path = "best_threshold.pkl"
    model = joblib.load(model_path)
    return model

try:
    model = load_model()

    # Show this toast only once per session
    if "core_loaded_toast_shown" not in st.session_state:
        st.toast("✅ ML Neural Core Loaded Successfully", icon="🔋")
        st.session_state["core_loaded_toast_shown"] = True

except Exception as e:
    st.error("❌ Could not load model. Make sure 'best_threshold.pkl' is in the same folder.")
    st.exception(e)
    st.stop()

# 🔐 Require access code before showing the dashboard
auth_gate()

# Show login success toast once, after auth
if st.session_state.get("auth_success"):
    st.toast("🔓 Access Granted — Welcome to SentinelSecure!", icon="🛡️")
    st.session_state["auth_success"] = False
# =========================
# 2. HELPER FUNCTIONS
# =========================

def normalize_label(raw_label):
    """
    Convert whatever the model outputs into either:
    - 'Intrusion'
    - 'Benign'

    Handles:
    - 0 / 1
    - strings like 'normal', 'attack', etc.
    """
    # Numeric
    if isinstance(raw_label, (int, float, np.integer, np.floating)):
        return "Intrusion" if int(raw_label) == 1 else "Benign"

    s = str(raw_label).strip().lower()
    if s in ["1", "attack", "intrusion", "malicious", "anomaly", "bad"]:
        return "Intrusion"
    if s in ["0", "normal", "benign", "good"]:
        return "Benign"

    # Fallback: treat unknown as Benign (safer for demo)
    return "Benign"


def recommend_action(label, score=None):
    """
    Given:
      - label: 'Intrusion' or 'Benign'
      - score: confidence (0–1) if available
    Returns: text like BLOCK / QUARANTINE / ALERT / ALLOW
    """
    if label == "Intrusion":
        if score is not None:
            if score >= 0.9:
                return "BLOCK"
            elif score >= 0.7:
                return "QUARANTINE"
            else:
                return "ALERT"
        else:
            return "BLOCK"
    else:  # Benign
        if score is not None and score >= 0.9:
            return "ALLOW"
        else:
            return "ALLOW (monitor)"


def build_analyst_summary(flow_dict, pred_label, action, score_display, explanation_text=None) -> str:
    """
    Build a plain-English justification for the decision so a security analyst
    can quickly understand and defend the action they take.
    """
    prot = flow_dict.get("protocol_type", "N/A")
    service = flow_dict.get("service", "N/A")
    flag = flow_dict.get("flag", "N/A")
    duration = flow_dict.get("duration", "N/A")
    src_bytes = flow_dict.get("src_bytes", "N/A")
    dst_bytes = flow_dict.get("dst_bytes", "N/A")
    count = flow_dict.get("count", "N/A")
    srv_count = flow_dict.get("srv_count", "N/A")

    conf_str = f"{score_display:.3f}" if score_display is not None else "N/A"

    lines = []

    lines.append("### Decision summary (for SOC analysts)")
    lines.append("")
    lines.append("**Flow context**")
    lines.append(f"- Protocol / Service / Flag: `{prot}` / `{service}` / `{flag}`")
    lines.append(f"- Duration: `{duration}`")
    lines.append(f"- Bytes: src_bytes=`{src_bytes}`, dst_bytes=`{dst_bytes}`")
    lines.append(f"- Recent activity: count=`{count}`, srv_count=`{srv_count}`")
    lines.append("")
    lines.append("**Model decision**")
    lines.append(f"- Classification: **{pred_label}**")
    lines.append(f"- Recommended response: **{action}**")
    lines.append(f"- Model confidence: **{conf_str}**")
    lines.append("")

    if pred_label == "Intrusion":
        lines.append("**Why this looks risky**")
        lines.append(
            "- The traffic pattern is similar to historical intrusion examples "
            "seen during model training (e.g., unusual duration, byte volume, or connection count)."
        )
        if explanation_text:
            lines.append("")
            lines.append("**Top contributing features (from XAI):**")
            for line in explanation_text.splitlines():
                lines.append(f"> {line}")
        lines.append("")
        lines.append("**How an analyst can justify this action**")
        if action == "BLOCK":
            lines.append(
                "- Blocking this flow prevents potential data exfiltration or lateral movement while "
                "we investigate the source host, without materially impacting normal business traffic."
            )
        elif action == "QUARANTINE":
            lines.append(
                "- Quarantining isolates the suspicious host/connection to limit blast radius, "
                "while preserving telemetry for forensic analysis."
            )
        else:  # ALERT or other
            lines.append(
                "- Raising a high-priority alert ensures this activity is manually reviewed and "
                "correlated with other events before any damage occurs."
            )
    else:  # Benign
        lines.append("**Why this is treated as benign**")
        lines.append(
            "- The pattern of protocol, service, duration and byte counts matches normal traffic "
            "seen in the training set, with no strong indicators of known attack behaviour."
        )
        lines.append("")
        lines.append("**How an analyst can justify allowing it**")
        if score_display is not None and score_display >= 0.9:
            lines.append(
                "- The model is highly confident this is normal, so blocking would risk unnecessary "
                "disruption without clear evidence of malicious intent."
            )
        else:
            lines.append(
                "- There is no strong evidence of an attack. The connection is allowed but can "
                "be monitored via existing logging and alerting rules."
            )

    return "\n".join(lines)


def run_model_on_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Core function:
    - Takes a DataFrame with (optionally) a 'label' column from training
    - Drops non-feature columns like 'label' and 'num_outbound_cmds'
    - Runs model.predict and (if supported) model.predict_proba
    - Adds columns: prediction_raw, label, score, recommended_action
    """
    # Keep original for display + download
    result = df.copy()

    # Build feature-only DataFrame for the model
    feature_df = df.copy()

    # Drop training label if present
    if "label" in feature_df.columns:
        feature_df = feature_df.drop(columns=["label"])

    # Model was trained WITHOUT this column
    if "num_outbound_cmds" in feature_df.columns:
        feature_df = feature_df.drop(columns=["num_outbound_cmds"])

    # Keep only numeric columns – model is fully numerical
    feature_df = feature_df.select_dtypes(include=["number"])

    # --- Prediction ---
    preds = model.predict(feature_df)
    result["prediction_raw"] = preds

    # --- Probability / confidence (if available) ---
    try:
        proba = model.predict_proba(feature_df)
        scores = proba.max(axis=1)
        result["score"] = scores.round(3)
    except Exception:
        pass

    # --- Normalize labels to 'Intrusion' / 'Benign' ---
    result["label"] = result["prediction_raw"].apply(normalize_label)

    # --- Recommended action ---
    if "score" in result.columns:
        result["recommended_action"] = [
            recommend_action(lbl, sc) for lbl, sc in zip(result["label"], result["score"])
        ]
    else:
        result["recommended_action"] = [
            recommend_action(lbl, None) for lbl in result["label"]
        ]

    return result

# =========================
# 3. SIDEBAR NAVIGATION
# =========================

with st.sidebar:
    st.markdown("""
        <div class="side-logo-tag">
            <span class="side-logo-dot"></span>
            SNTL-SEC · NODE-01
        </div>
        <div class="side-title">console / nav</div>
        <div class="side-subtitle">select operating zone</div>
    """, unsafe_allow_html=True)

page = st.sidebar.radio(
    "Go to:",
    ["Bulk Analysis", "Attack Playground", "Attack Simulator (what-if)", "Model & Evaluation"]
)

st.sidebar.markdown(
    """
    <div class="side-info-box">
        <strong>SentinelSecure v0.1</strong><br/><br/>
        • Upload CSVs with the SAME columns as the training data<br/>
        • Model + thresholds are for demo, not production<br/>
        • Threat ledger is an in-memory, hash-chained audit trail
    </div>
    """,
    unsafe_allow_html=True
)
# --- Logout control ---
st.sidebar.markdown("---")
if st.sidebar.button("Logout", use_container_width=True):
    # reset auth flags
    st.session_state["authenticated"] = False
    st.session_state["auth_success"] = False
    try:
        st.rerun()
    except Exception:
        try:
            st.experimental_rerun()
        except Exception:
            pass

# =========================
# 4. BULK ANALYSIS PAGE
# =========================

if page == "Bulk Analysis":
    st.subheader("📂 Bulk CSV Intrusion Analysis")

    uploaded_file = st.file_uploader(
        "Upload network flows CSV",
        type=["csv"],
        help="Use the same schema/columns as the dataset used in the notebook."
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error("Could not read the CSV file. Check encoding / format.")
            st.exception(e)
            st.stop()

        st.write("### Preview of uploaded data")
        st.dataframe(df.head(), use_container_width=True)

        # Tiny neon loader + spinner while running model
        loader_placeholder = st.empty()
        loader_placeholder.markdown(
            '<div class="neon-loader"><div class="neon-loader-bar"></div></div>',
            unsafe_allow_html=True
        )

        with st.spinner("Running intrusion detection on uploaded flows..."):
            results = run_model_on_df(df)

        loader_placeholder.empty()

        st.success(f"Analysis complete. Total flows: {len(results)}")

        # 🔥 Live Threat Feed (latest intrusions)
        st.markdown("### 🔥 Live Threat Feed (latest intrusions)")
        intrusions_feed = results[results["label"] == "Intrusion"].copy()
        if intrusions_feed.empty:
            st.caption("No intrusions detected in this batch.")
        else:
            # Sort by confidence if available
            if "score" in intrusions_feed.columns:
                intrusions_feed = intrusions_feed.sort_values("score", ascending=False)

            # Choose key columns for the feed (only if they exist)
            feed_cols = []
            for col in [
                "label",
                "score",
                "recommended_action",
                "protocol_type",
                "service",
                "src_bytes",
                "dst_bytes",
                "duration",
            ]:
                if col in intrusions_feed.columns:
                    feed_cols.append(col)
            if not feed_cols:
                feed_cols = intrusions_feed.columns.tolist()

            feed_df = intrusions_feed[feed_cols].head(30)
            feed_html = feed_df.to_html(index=False, classes="threat-table")
            st.markdown(
                f"""
                <div class="threat-feed-container">
                    <div class="threat-feed">
                        {feed_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Simple metrics
        col1, col2, col3 = st.columns(3)
        total_intrusions = (results["label"] == "Intrusion").sum()
        total_benign = (results["label"] == "Benign").sum()
        intrusion_pct = (total_intrusions / len(results) * 100) if len(results) > 0 else 0

        col1.metric("Total Intrusions", total_intrusions, delta_color="inverse")
        col2.metric("Benign Flows", total_benign)
        col3.metric("Intrusion %", f"{intrusion_pct:.2f}%")

        # Blinking intrusion indicator
        if total_intrusions > 0:
            st.markdown(
                f"""
                <div class="intrusion-indicator">
                    <span class="intrusion-indicator-dot"></span>
                    <span>ACTIVE INTRUSIONS DETECTED · {total_intrusions}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("### Detailed Results")
        st.dataframe(results, use_container_width=True)

        # Option to download
        csv_out = results.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download results as CSV",
            data=csv_out,
            file_name="sentinelsecure_bulk_results.csv",
            mime="text/csv",
        )

        # ---------- ⛓️ Commit intrusions to threat ledger ----------
        if add_log is not None:
            intrusions = results[results["label"] == "Intrusion"]

            if not intrusions.empty:
                st.markdown("### ⛓️ Threat Ledger")
                if st.button("Commit all detected intrusions to ledger"):
                    committed = 0
                    for idx, row in intrusions.iterrows():
                        row_dict = row.to_dict()
                        features_only = {
                            k: v for k, v in row_dict.items()
                            if k not in ["prediction_raw", "label", "score", "recommended_action"]
                        }

                        entry = {
                            "flow_index": int(idx),
                            "label": row_dict.get("label"),
                            "recommended_action": row_dict.get("recommended_action"),
                            "confidence": float(row_dict["score"]) if "score" in row_dict else None,
                            "features": features_only,
                        }
                        add_log(entry)
                        committed += 1

                    st.success(f"✅ Committed {committed} intrusion logs to the in-memory threat ledger.")
                    if verify_chain is not None:
                        st.caption(
                            f"Ledger integrity: "
                            f"{'✅ valid' if verify_chain() else '⚠️ chain broken (hash mismatch)'}"
                        )

                # Optional: view the ledger
                if get_chain_as_list is not None:
                    with st.expander("View current threat ledger (debug view)"):
                        st.json(get_chain_as_list())
            else:
                st.info("No intrusions detected in this batch to commit to the ledger.")
        else:
            st.caption("⚠️ ledger.py not available – threat ledger features disabled.")
    else:
        st.info("Upload a CSV file to run bulk intrusion analysis.")

# =========================
# 5. ATTACK PLAYGROUND PAGE
# =========================

elif page == "Attack Playground":
    st.subheader("🎯 Attack Playground")

    st.markdown(
        "Upload a CSV with one or more flows. "
        "You can then pick a single row to **inspect deeply**, "
        "see the **prediction**, the **explanation**, and "
        "append it to the **tamper-evident threat ledger**."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV for playground",
        type=["csv"],
        key="playground_uploader",
        help="Same schema as training dataset. We'll let you pick a row."
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error("Could not read the CSV file.")
            st.exception(e)
            st.stop()

        if df.empty:
            st.warning("The uploaded CSV is empty.")
            st.stop()

        st.write("### Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Let user choose a row to inspect
        st.write("### Choose a flow to inspect")
        if "row_index" not in st.session_state:
            st.session_state["row_index"] = 0

        row_index = st.number_input(
             "Row index (0-based)",
            min_value=0,
            max_value=len(df) - 1,
            value=st.session_state["row_index"],
            step=1,
            key="row_index_input"
        )

        selected_row = df.iloc[[row_index]]  # keep as DataFrame for model

        st.write("#### Selected flow (raw features)")
        st.json(selected_row.iloc[0].to_dict())

        # Run prediction on that single row
        with st.spinner("Classifying selected flow..."):
            res_single = run_model_on_df(selected_row)

        pred_label = res_single["label"].iloc[0]
        action = res_single["recommended_action"].iloc[0]
        score_display = res_single["score"].iloc[0] if "score" in res_single.columns else None

        col1, col2, col3 = st.columns(3)
        col1.metric("Prediction", pred_label)
        col2.metric("Recommended Action", action)
        if score_display is not None:
            col3.metric("Confidence", f"{score_display:.3f}")
        else:
            col3.metric("Confidence", "N/A (no predict_proba)")

        st.write("#### Model output (technical view)")
        st.dataframe(res_single, use_container_width=True)

        # ---------- 🔍 Explainable AI section ----------
        st.write("### 🧠 Why did the model say this? (XAI)")

        explanation_text = None
        reasons = []

        if explain_flow is None:
            st.warning(
                "Explainability module could not be imported. "
                "Check explain.py and that it's in the same folder."
            )
        else:
            try:
                flow_dict = selected_row.iloc[0].to_dict()
                explanation_text = explain_flow(flow_dict, top_n=5)
                st.code(explanation_text, language="markdown")

                # Parse technical explanation into (feature, value, importance)
                for line in explanation_text.splitlines():
                    # Expecting lines like: "- feature: value=X, importance=Y"
                    if line.startswith("- ") and "importance=" in line:
                        try:
                            body = line[2:]  # strip "- "
                            name_part, rest = body.split(":", 1)
                            name = name_part.strip()

                            val_str = None
                            imp_str = None
                            if "value=" in rest:
                                val_str = rest.split("value=", 1)[1].split(",", 1)[0].strip()
                            if "importance=" in rest:
                                imp_str = rest.split("importance=", 1)[1].strip()

                            reasons.append((name, val_str, imp_str))
                        except Exception:
                            continue

            except Exception as e:
                st.error("Explainability failed at runtime.")
                st.exception(e)

        if load_error:
            st.caption(f"ℹ️ explain.py model note: {load_error}")

        # ---------- 📌 Simplified Analyst Summary ----------
        st.write("### 📌 Simplified Analyst Summary")
        if simple_explanation is not None and reasons:
            simple_msg = simple_explanation(pred_label, score_display, reasons)
            st.success(simple_msg)
        elif simple_explanation is None:
            st.caption("simple_explanation function not available in explain.py.")
        else:
            st.caption("No detailed feature importance available to build a summary.")

        # ---------- 🧾 Analyst-friendly justification ----------
        st.write("### 📄 Analyst-friendly justification")

        if st.button("Generate simplified justification text"):
            justification = build_analyst_summary(
                flow_dict=selected_row.iloc[0].to_dict(),
                pred_label=pred_label,
                action=action,
                score_display=score_display,
                explanation_text=explanation_text,
            )
            st.markdown(justification)

        # ---------- 🔗 Threat Ledger log ----------
        st.write("### 🔗 Threat Ledger Block")

        if add_log is None:
            st.caption("⚠️ ledger.py not available – cannot append to threat ledger.")
        else:
            flow_dict = selected_row.iloc[0].to_dict()
            entry = {
                "flow_index": int(row_index),
                "label": pred_label,
                "recommended_action": action,
                "confidence": float(score_display) if score_display is not None else None,
                "features": flow_dict,
            }

            block = add_log(entry)
            chain_ok = verify_chain() if verify_chain is not None else None

            st.json({
                "block_index": block["index"],
                "timestamp": block["timestamp"],
                "hash": block["hash"],
                "prev_hash": block["prev_hash"],
                "chain_valid": chain_ok,
            })

            st.caption(
                "This block is now part of an append-only, hash-chained audit trail "
                "for security incidents."
            )

    else:
        st.info("Upload a CSV to play with individual flows.")

# =========================
# 6. ATTACK SIMULATOR (WHAT-IF)
# =========================

elif page == "Attack Simulator (what-if)":
    st.subheader("🧪 Attack Simulator (What-if Sandbox)")

    st.markdown(
        "Instead of replaying a stream, this sandbox lets you **manually tweak key flow features** "
        "to see **when the model flips from Benign → Intrusion** (and how severe the response is).\n\n"
        "1. Upload a CSV with flows (same schema as training).\n"
        "2. Pick a base flow.\n"
        "3. Adjust numeric sliders (duration, bytes, rates, etc.).\n"
        "4. Compare original vs simulated prediction + XAI explanation."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV for simulation",
        type=["csv"],
        key="simulator_uploader",
        help="Use the same schema / columns as the training dataset."
    )

    if uploaded_file is not None:
        try:
            df_sim = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error("Could not read the CSV file.")
            st.exception(e)
            st.stop()

        if df_sim.empty:
            st.warning("The uploaded CSV is empty.")
            st.stop()

        st.write("### Sample of uploaded flows")
        st.dataframe(df_sim.head(), use_container_width=True)

        # ----- Choose base row -----
        st.write("### Step 1: Choose a base flow")

        if "sim_row_index" not in st.session_state:
            st.session_state.sim_row_index = 0

        row_index = st.number_input(
            "Row index (0-based)",
            min_value=0,
            max_value=len(df_sim) - 1,
            value=st.session_state.sim_row_index,
            step=1,
            key="sim_row_index_input"
        )
        st.session_state.sim_row_index = row_index

        base_row = df_sim.iloc[int(row_index)].copy()
        st.write(f"#### Base flow #{int(row_index)} (raw features)")
        st.json(base_row.to_dict())

        # ----- Baseline model prediction on the original row -----
        with st.spinner("Classifying base flow..."):
            base_res = run_model_on_df(pd.DataFrame([base_row]))

        base_label = base_res["label"].iloc[0]
        base_action = base_res["recommended_action"].iloc[0]
        base_score = base_res["score"].iloc[0] if "score" in base_res.columns else None

        st.write("### Baseline model decision (original flow)")
        c1, c2, c3 = st.columns(3)
        c1.metric("Baseline Prediction", base_label)
        c2.metric("Baseline Action", base_action)
        if base_score is not None:
            c3.metric("Baseline Confidence", f"{base_score:.3f}")
        else:
            c3.metric("Baseline Confidence", "N/A")

        st.markdown("---")

        # ----- Step 2: Let the user tweak key numeric features -----
        st.write("### Step 2: Tweak key features and simulate")

        sim_row = base_row.copy()
        updated_values = {}

        st.write("#### Core volume / frequency features")
        col_int1, col_int2, col_int3 = st.columns(3)
        with col_int1:
            if "duration" in df_sim.columns:
                updated_values["duration"] = st.slider(
                    "duration (connection length)",
                    min_value=0,
                    max_value=int(max(1, df_sim["duration"].max() * 2)),
                    value=int(base_row["duration"]),
                    step=1,
                )
        with col_int2:
            if "src_bytes" in df_sim.columns:
                updated_values["src_bytes"] = st.slider(
                    "src_bytes (bytes from source)",
                    min_value=0,
                    max_value=int(max(1000, df_sim["src_bytes"].quantile(0.95) * 2)),
                    value=int(base_row["src_bytes"]),
                    step=1,
                )
        with col_int3:
            if "dst_bytes" in df_sim.columns:
                updated_values["dst_bytes"] = st.slider(
                    "dst_bytes (bytes to destination)",
                    min_value=0,
                    max_value=int(max(1000, df_sim["dst_bytes"].quantile(0.95) * 2)),
                    value=int(base_row["dst_bytes"]),
                    step=1,
                )

        col_int4, col_int5 = st.columns(2)
        with col_int4:
            if "count" in df_sim.columns:
                updated_values["count"] = st.slider(
                    "count (connections to same host)",
                    min_value=0,
                    max_value=int(max(10, df_sim["count"].quantile(0.95) * 2)),
                    value=int(base_row["count"]),
                    step=1,
                )
        with col_int5:
            if "srv_count" in df_sim.columns:
                updated_values["srv_count"] = st.slider(
                    "srv_count (connections to same service)",
                    min_value=0,
                    max_value=int(max(10, df_sim["srv_count"].quantile(0.95) * 2)),
                    value=int(base_row["srv_count"]),
                    step=1,
                )

        st.write("#### Error / anomaly rate features (0.0 – 1.0)")
        col_rate1, col_rate2, col_rate3 = st.columns(3)
        with col_rate1:
            if "serror_rate" in df_sim.columns:
                updated_values["serror_rate"] = st.slider(
                    "serror_rate",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(base_row["serror_rate"]),
                    step=0.01,
                )
        with col_rate2:
            if "srv_serror_rate" in df_sim.columns:
                updated_values["srv_serror_rate"] = st.slider(
                    "srv_serror_rate",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(base_row["srv_serror_rate"]),
                    step=0.01,
                )
        with col_rate3:
            if "same_srv_rate" in df_sim.columns:
                updated_values["same_srv_rate"] = st.slider(
                    "same_srv_rate",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(base_row["same_srv_rate"]),
                    step=0.01,
                )

        col_rate4, col_rate5, col_rate6 = st.columns(3)
        with col_rate4:
            if "diff_srv_rate" in df_sim.columns:
                updated_values["diff_srv_rate"] = st.slider(
                    "diff_srv_rate",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(base_row["diff_srv_rate"]),
                    step=0.01,
                )
        with col_rate5:
            if "dst_host_same_srv_rate" in df_sim.columns:
                updated_values["dst_host_same_srv_rate"] = st.slider(
                    "dst_host_same_srv_rate",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(base_row["dst_host_same_srv_rate"]),
                    step=0.01,
                )
        with col_rate6:
            if "dst_host_srv_diff_host_rate" in df_sim.columns:
                updated_values["dst_host_srv_diff_host_rate"] = st.slider(
                    "dst_host_srv_diff_host_rate",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(base_row["dst_host_srv_diff_host_rate"]),
                    step=0.01,
                )

        st.markdown("When you're ready, run the simulated flow through the model:")

        if st.button("🚀 Run simulation with updated values"):
            # Apply the updated values into a copy of the base row
            for k, v in updated_values.items():
                sim_row[k] = v

            sim_df = pd.DataFrame([sim_row])

            with st.spinner("Classifying simulated flow..."):
                sim_res = run_model_on_df(sim_df)

            sim_label = sim_res["label"].iloc[0]
            sim_action = sim_res["recommended_action"].iloc[0]
            sim_score = sim_res["score"].iloc[0] if "score" in sim_res.columns else None

            st.markdown("### 🔍 Comparison: Original vs Simulated")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Original flow**")
                st.metric("Prediction", base_label)
                st.metric("Action", base_action)
                st.metric("Confidence", f"{base_score:.3f}" if base_score is not None else "N/A")
            with col_b:
                st.markdown("**Simulated flow**")
                st.metric("Prediction", sim_label)
                st.metric("Action", sim_action)
                st.metric("Confidence", f"{sim_score:.3f}" if sim_score is not None else "N/A")

            st.write("#### Simulated flow (full feature view)")
            st.json(sim_row.to_dict())

            # ---------- XAI on the simulated flow ----------
            st.write("### 🧠 Why did the model say this? (XAI on simulated flow)")

            explanation_text = None
            reasons = []

            if explain_flow is None:
                st.warning(
                    "Explainability module could not be imported. "
                    "Check explain.py and that it's in the same folder."
                )
            else:
                try:
                    explanation_text = explain_flow(sim_row.to_dict(), top_n=5)
                    st.code(explanation_text, language="markdown")

                    # Parse into reasons for simple_explanation
                    if explanation_text:
                        for line in explanation_text.splitlines():
                            if line.startswith("- ") and "importance=" in line:
                                try:
                                    body = line[2:]
                                    name_part, rest = body.split(":", 1)
                                    name = name_part.strip()

                                    val_str = None
                                    imp_str = None
                                    if "value=" in rest:
                                        val_str = rest.split("value=", 1)[1].split(",", 1)[0].strip()
                                    if "importance=" in rest:
                                        imp_str = rest.split("importance=", 1)[1].strip()

                                    reasons.append((name, val_str, imp_str))
                                except Exception:
                                    continue
                except Exception as e:
                    st.error("Explainability failed at runtime.")
                    st.exception(e)

            if load_error:
                st.caption(f"ℹ️ explain.py model note: {load_error}")

            st.write("### 📌 Simplified Analyst Summary (simulated flow)")
            if simple_explanation is not None and reasons:
                simple_msg = simple_explanation(sim_label, sim_score, reasons)
                st.success(simple_msg)
            elif simple_explanation is None:
                st.caption("simple_explanation function not available in explain.py.")
            else:
                st.caption("No detailed feature importance available to build a summary.")

            st.write("### 📄 Analyst-friendly justification (simulated flow)")
            justification = build_analyst_summary(
                flow_dict=sim_row.to_dict(),
                pred_label=sim_label,
                action=sim_action,
                score_display=sim_score,
                explanation_text=explanation_text,
            )
            st.markdown(justification)

    else:
        st.info("Upload a CSV to build and simulate custom flows.")

# =========================
# 7. MODEL & EVALUATION PAGE
# =========================

elif page == "Model & Evaluation":
    st.subheader("📊 Model Performance & Evaluation")

    st.markdown("""
    ### Model Summary

    - **Algorithm**: XGBoost Classifier + LightGBM   
    - **Dataset**: Sanitized network flow dataset (e.g., NSL-KDD / CIC-IDS 2017)  
    - **Objective**: Prioritize **Recall** on the Intrusion class (minimize missed attacks).

    
    """)

    st.markdown("""
    ### Validation Metrics (Hold-out set)

    - Accuracy: **80%**  
    - Precision (Intrusion): **80.18%**  
    - Recall (Intrusion): **98.73%**  
    - F1-score (Intrusion): **88.49%**

    """)

    st.markdown("""
    ### Why Recall First?

    - In a SOC environment, a **missed intrusion (false negative)** is more dangerous
      than an extra alert (false positive).  
    - We tune the model threshold and class weights so that **intrusions are rarely missed**,
      then rely on the dashboard + action logic (BLOCK / QUARANTINE / ALERT) to help
      analysts triage noisy or low-confidence cases.
    """)

    st.markdown("""
    """)
