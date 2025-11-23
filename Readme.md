# 🛡️ SentinelSecure v1  
AI/ML Real-Time Network Intrusion Detection & Triage System  
🚨 Built for Redact Hackathon 2025 – CyberSecure Theme

---

## ⚡ Overview

Security teams receive too many alerts to manually triage.  
**SentinelSecure** provides an **automated first layer of defence**:

✔ Detects malicious vs. normal network traffic  
✔ High **Recall** — avoids missed attacks  
✔ Automated **security action suggestions**  
✔ Explainable AI (**why** it was flagged)  
✔ Blockchain-style hash-chained threat ledger  
✔ Cyberpunk SOC dashboard 🌐

---

## 🛠️ Tech Stack
- Streamlit UI
- ML Model trained on Network Intrusion Dataset
- XGBoost classifier
- SHAP-based interpretability
- In-memory blockchain log (SHA-256 chaining)

---

## 📈 Model Focus: Recall First

| Metric | Intrusion Class |
|--------|----------------|
| Recall | **98.73%** ← Most important |
| Precision | 80.18% |
| F1-Score | 88.49% |
| Accuracy | 80% |

> Fill in with numbers from your Jupyter training results.

Why Recall?  
Missed attacks = security breaches.  
False alerts = manageable.

---

## ⚙️ Run Instructions (Judging Guide)

### 1️⃣ System Requirements
- Python **3.10 or 3.11 recommended**
- Git + Stable Internet

### 2️⃣ Setup

```bash
git clone https://github.com/YOUR_USERNAME/SentinelSecure.git
cd SentinelSecure

python -m venv venv
# Windows
venv\Scripts\
just write activate
# Mac/Linux
source venv/bin/
just write activate


the python virtual environment (venv) will open
navigate back to the folder containing app.py or you may get error.
pip install -r requirements.txt
streamlit run app.py

Browser will auto-open:
http://localhost:8501/

3️⃣ Access Code
sentinel-sec-24

📦 Repository Structure
📦 SentinelSecure
 ├── app.py                  # Streamlit cyberpunk dashboard UI
 ├── best_threshold.pkl      # Trained XGBoost intrusion model
 ├── explain.py              # SHAP/XAI feature explanation
 ├── ledger.py               # Hash-chained blockchain logger
 ├── sample_flows.csv        # Demo dataset for judges
 ├── requirements.txt
 └── README.md

🧩 Key Modules
Module	Purpose
Bulk Analysis	Analyze entire CSVs of network flows
Attack Playground	Investigate single events with XAI
What-If Attack Simulator	Modify features to trigger intrusion
Threat Ledger	Tamper-evident incident history

💎 Highlights for Judges
Working Prototype — full end-to-end demonstration

Automation of analyst decisions

Explainability — “why model thinks it’s an intrusion”

Blockchain — immutable audit trail

UX Design — professional SOC interface

⚡ Optimized for hackathon scoring — zero PPT, full live demo.

👥 Team
Team : Smart Coders
Members: Vinit (Leader) + Pratham + Saurav