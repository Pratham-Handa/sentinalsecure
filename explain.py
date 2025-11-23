# explain.py  (same folder as app.py + best_threshold.pkl)

import os

try:
    import pandas as pd
except Exception:
    pd = None

try:
    import joblib
except Exception:
    joblib = None

MODEL_PATH = "best_threshold.pkl"

model = None
load_error = None
feature_error = None
explainer_init_error = None  # kept for compatibility with app.py


# ----------------- Load model -----------------
if joblib is None:
    load_error = "joblib not installed - cannot load model."
else:
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            load_error = f"Model file not found at: {MODEL_PATH}"
    except Exception as e:
        load_error = f"Could not load model: {e}"


# ----------------- KNOWN FEATURE ORDER (from training) -----------------
# This must match EXACTLY the order the model was trained with.
FEATURE_ORDER = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "land",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    # NOTE: no num_outbound_cmds here for this model
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_count",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
]


# ----------------- Helper: find underlying XGBoost booster -----------------
def _get_xgb_booster(m):
    """
    Try to locate an underlying XGBoost booster, even if the
    model is wrapped in a StackingClassifier or other meta-estimator.
    """
    if m is None:
        return None, "Model is None, cannot get booster."

    # Case 1: direct XGBClassifier / XGBModel
    if hasattr(m, "get_booster"):
        try:
            return m.get_booster(), None
        except Exception as e:
            return None, f"Calling get_booster() on model failed: {e}"

    # Case 2: Stacking / meta-estimators with final_estimator_
    if hasattr(m, "final_estimator_") and hasattr(m.final_estimator_, "get_booster"):
        try:
            return m.final_estimator_.get_booster(), None
        except Exception as e:
            return None, f"Calling get_booster() on final_estimator_ failed: {e}"

    # Case 3: ensemble with a list of estimators_ (take first XGBoost-like one)
    if hasattr(m, "estimators_"):
        for est in m.estimators_:
            if hasattr(est, "get_booster"):
                try:
                    return est.get_booster(), None
                except Exception:
                    continue

    return None, "No underlying XGBoost booster with get_booster() found in this model."


def _row_to_dataframe(flow_row: dict):
    """Convert a single flow dict into a 1-row DataFrame with the model's feature order."""
    if pd is None:
        return None
    if not FEATURE_ORDER:
        return None

    row_vals = [flow_row.get(col, 0) for col in FEATURE_ORDER]
    return pd.DataFrame([row_vals], columns=FEATURE_ORDER)


def simple_explanation(label, score, reasons):
    """
    Turn technical feature-importance info into a short,
    human-friendly justification for security analysts.
    `reasons` is a list of (feature_name, value, importance).
    """
    lines = []

    # 1) Heading based on label
    if str(label).lower() == "intrusion":
        lines.append("⚠️ High-risk traffic detected.")
    else:
        lines.append("✔️ Traffic classified as benign.")

    # 2) Confidence
    if score is not None:
        try:
            confidence_pct = round(float(score) * 100, 1)
            lines.append(f"Model confidence: {confidence_pct}%.")
        except Exception:
            pass

    # 3) Top reasons
    if reasons:
        lines.append("")
        lines.append("Key reasons:")
        for name, val, imp in reasons:
            pretty_name = name.replace("_", " ").title()
            try:
                imp_f = float(imp)
            except Exception:
                imp_f = 0.0

            # Rough direction text
            direction = "strong influence" if abs(imp_f) > 0.1 else "moderate influence"
            lines.append(f"- {pretty_name} = {val}  ({direction})")
    else:
        lines.append("")
        lines.append("The model did not expose detailed feature contributions for this flow.")

    # 4) Action guidance
    lines.append("")
    if str(label).lower() == "intrusion":
        if score is not None and float(score) >= 0.9:
            lines.append("Recommended response: **Block immediately** and open an incident ticket.")
        elif score is not None and float(score) >= 0.7:
            lines.append("Recommended response: **Quarantine** this source and monitor closely.")
        else:
            lines.append("Recommended response: Raise an **alert** for analyst review.")
    else:
        lines.append("Recommended response: **Allow** but keep the flow logged for future audits.")

    return "\n".join(lines)

    """
    Converts technical feature importance explanation into a short,
    business-friendly interpretation for security analysts.
    """
    if label.lower() == "intrusion":
        risk_word = "⚠️ High Risk Traffic Detected"
    else:
        risk_word = "✔️ Safe/Benign Traffic"
    
    lines = []
    lines.append(f"{risk_word}")
    
    if score is not None:
        confidence_pct = round(float(score) * 100, 1)
        lines.append(f"Model confidence: {confidence_pct}%")

    if reasons:
        lines.append("Likely due to:")
        for name, val, impact in reasons:
            name_fmt = name.replace("_", " ").title()
            direction = "↑" if float(val) > 0 else ""
            lines.append(f"• {name_fmt} ({val}) {direction}")
    else:
        lines.append("Model could not identify clear contributing factors.")

    if label.lower() == "intrusion":
        lines.append("\nRecommended response:")
        if score and score >= 0.9:
            lines.append("→ Immediate block to prevent potential threat.")
        elif score and score >= 0.7:
            lines.append("→ Quarantine and monitor further behavior.")
        else:
            lines.append("→ Alert analyst for deeper inspection.")
    else:
        lines.append("\nRecommended response: Allow but log for audit.")

    return "\n".join(lines)


def explain_flow(flow_row: dict, top_n: int = 5) -> str:
    """
    XAI via XGBoost feature importance:
    - Uses model's global feature importance (gain)
    - Maps XGBoost internal feature ids (e.g. 'f0') to your NSL-KDD feature names
    - For top N features, shows importance + this flow's value.
    """
    lines = []

    if model is None:
        lines.append("Model not available for explanation.")
        if load_error:
            lines.append(load_error)
        return "\n".join(lines)

    if not FEATURE_ORDER:
        lines.append("FEATURE_ORDER is empty - cannot map inputs to features.")
        return "\n".join(lines)

    booster, booster_err = _get_xgb_booster(model)
    if booster is None:
        lines.append("Could not access underlying XGBoost booster for feature importance.")
        if booster_err:
            lines.append(booster_err)
        return "\n".join(lines)

    # ---------- Global feature importance from XGBoost ----------
    try:
        # importance_type can be: "weight", "gain", "cover", "total_gain", "total_cover"
        raw_importance = booster.get_score(importance_type="gain")
    except Exception as e:
        lines.append("Could not compute feature importance from XGBoost booster.")
        lines.append(str(e))
        return "\n".join(lines)

    if not raw_importance:
        lines.append("Model returned empty feature importance. Falling back to raw feature values.")
        for name in FEATURE_ORDER:
            lines.append(f"- {name}: {flow_row.get(name)}")
        return "\n".join(lines)

    # Map keys like 'f0', 'f1', ... to human feature names using FEATURE_ORDER
    mapped_importance = []
    for key, imp in raw_importance.items():
        # XGBoost usually uses 'f0', 'f1', ... as keys if there was no column name
        if key.startswith("f"):
            try:
                idx = int(key[1:])
                if 0 <= idx < len(FEATURE_ORDER):
                    fname = FEATURE_ORDER[idx]
                else:
                    fname = key  # fallback
            except Exception:
                fname = key
        else:
            # if keys already match actual column names
            fname = key

        mapped_importance.append((fname, float(imp)))

    # Sort by importance descending
    mapped_importance.sort(key=lambda x: x[1], reverse=True)
    top = mapped_importance[:top_n]

    lines.append("Top model features (XGBoost gain importance):")
    for fname, imp in top:
        val = flow_row.get(fname)
        lines.append(f"- {fname}: value={val}, importance={round(float(imp), 6)}")

    # ---------- Optional: predicted probabilities for this flow ----------
    try:
        if pd is not None and hasattr(model, "predict_proba"):
            df_row = _row_to_dataframe(flow_row)
            if df_row is not None:
                proba = model.predict_proba(df_row)[0]
                lines.append("")
                lines.append(
                    f"Predicted class probabilities [Benign, Intrusion]: {proba.tolist()}"
                )
    except Exception:
        # Safe to ignore errors here
        pass

    return "\n".join(lines)
