# 🛡️ SentinelSecure v0.1  
**AI/ML Real-Time Network Intrusion Detection & Triage System**  
Built for 🚨 *Redact Hackathon 2025 – CyberSecure Problem Statement*

---

## ⚡ Overview

Modern SOCs are overwhelmed by alerts. **SentinelSecure** acts as the **first automated triage layer** for network threat detection.

📌 The system:
- Detects **Intrusion vs Benign** network flows using ML
- Minimizes **false negatives (high Recall)**
- Suggests **context-aware security actions**
- Logs threats in an **immutable hash-chained ledger**
- Provides **Explainable AI** reasons for every alert
- Features a **professional cyberpunk SOC dashboard**

> Designed for speed, clarity, and analyst-oriented decision support.

---

## 🧠 Core Features

| Capability | Description |
|-----------|-------------|
| **ML Intrusion Classifier** | Binary model trained on network flow features |
| **Priority = Recall** | Avoids missed attacks by aggressive threat detection tuning |
| 🧪 **Bulk CSV Analysis** | Upload entire flow batches → classification + download |
| 🎯 **Attack Playground** | Investigate flows individually with XAI insights |
| 🔄 **What-If Attack Simulator** | Modify features → observe flip from benign to intrusion |
| 🔐 **Access Gate** | Authorization required to enter console |
| 🔗 **Threat Ledger** | Blockchain-style hash chaining for tamper-evident logs |
| ✨ **Cyberpunk SOC UI** | Animated indicators, neon metrics, live threat feed |

---

## 🧩 Architecture Diagram

Network Flow CSV
│
▼
ML Model → Prediction → Action Logic (BLOCK / QUARANTINE / ALERT / ALLOW)
│
├── XAI (Why flagged?)
└── Threat Ledger (Hash-secured audit chain)

yaml
Copy code

---

## 📈 Performance (Validation Set)

> Fill with your actual metrics before presenting — judges 🔥 this section!

| Metric | Intrusion Class |
|--------|----------------|
| **Recall** | `TBD` ← Most Important |
| Precision | `TBD` |
| F1-Score | `TBD` |
| Accuracy | `TBD` |

Why Recall?  
> Missing a real intrusion (False Negative) is more dangerous than blocking a benign flow.

---

## 🛠️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
Open browser → http://localhost:8501/

🔑 Console Access Code:

matlab
Copy code
sentinel-sec-24
📦 Folder Structure
bash
Copy code
📦 SentinelSecure
 ├── app.py                  # Streamlit dashboard UI + logic
 ├── explain.py              # XAI helper (SHAP-like feature contribution)
 ├── ledger.py               # Hash-chained logging (simulated blockchain)
 ├── best_threshold.pkl      # Trained ML model
 ├── sample_flows.csv        # Demo dataset
 ├── requirements.txt
 └── README.md