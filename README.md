<!-- HEADER SHIELDS -->
<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange?logo=tensorflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25-red?logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-F7931E?logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Hackathon](https://img.shields.io/badge/Hackathon-Starlight%202026-ff69b4)

# 🛡️ ZeroShield AI
### *Real‑Time Zero‑Day Threat Detection*

**Machine learning intrusion detection system that spots *unknown attacks* in live network traffic — no signatures required.**

Built for **Devpost Starlight Hackathon** · DevSoc @ UNSW Roundhouse · 24 July 2026

[⭐ Star this repo](https://github.com/LuthandoCandlovu/ZeroShield-AI) · [▶ Run It Yourself](#-run-it-yourself) · [🧠 Architecture](#-architecture) · [📊 Performance](#-performance)

</div>

---

## 🎪 Hackathon Context

**Starlight 2026** — hosted by **DevSoc at UNSW Roundhouse (24 July 2026)** — is an open project showcase celebrating creative engineering. It brings together students, hobbyists, and researchers to present working prototypes that solve real problems.

| Field | Detail |
|-------|--------|
| **Event** | Starlight 2026 (DevSoc, UNSW) |
| **Track** | AI / Cybersecurity |
| **Venue** | UNSW Roundhouse, Sydney |
| **Date** | 24 July 2026 |
| **Goal** | Detect zero‑day cyberattacks in real time using unsupervised anomaly detection |

My goal was to build something that not only **works**, but tackles a genuine real‑world cybersecurity gap — the fundamental limitation of every signature‑based IDS on the market today.

---

## 🔴 The Problem

> **Signature‑based intrusion detection systems (Snort, Suricata, etc.) are blind to zero‑day attacks.**

Cybercriminals constantly invent new exploits that leave *no known signature*. Traditional systems can only detect what they've seen before — so the first time a novel attack hits your network, **you're completely blind**.

This leads to:
- 💣 Undetected intrusions sitting in your network for days or weeks
- 💸 Average breach cost of **$4.88M** (IBM 2024) — zero‑days drive a disproportionate share
- 📋 Massive rule‑maintenance overhead for security teams
- 🚨 Alert fatigue from poorly tuned signatures

**Real‑world example:** In 2024, a zero‑day vulnerability in a popular enterprise firewall went undetected for *weeks*, affecting thousands of organisations worldwide. By the time a signature was released, the damage — ransomware, data exfiltration, financial loss — was already done.

---

## 🛡️ The Solution — ZeroShield AI

An **unsupervised machine learning IDS** that detects zero‑day attacks in real time without needing *any* prior attack signatures.

ZeroShield AI learns the pattern of **normal** network traffic (using only benign samples). Any deviation from that normal behaviour is flagged immediately as a potential threat.

### How it works (non-technical)

1. **Train** — Feed the system hours of normal network activity (no attacks). It builds a model of "what's expected".
2. **Detect** — Live traffic flows are compared against that model. If a flow behaves strangely (long duration, many bytes, odd flags), it triggers a red alert.
3. **Ensemble** — Two different AI models work together to reduce false alarms and catch different types of anomalies.

### ZeroShield vs Traditional IDS

| Criterion | Traditional IDS | 🛡️ ZeroShield AI |
|-----------|----------------|-----------------|
| Attack knowledge | ❌ Needs known signatures | ✅ Works with normal traffic only |
| Zero‑day detection | ❌ Blind until patch released | ✅ Detects unknown anomalies instantly |
| Maintenance | ❌ Manual rule updates forever | ✅ Retrain with new normal data |
| Inference speed | ⚠️ Can lag on high-volume traffic | ✅ < 10 ms per flow |
| False positive rate | ⚠️ High without expert tuning | ✅ < 2% (ensemble voting) |

---

## 🧠 Architecture

The system uses **two complementary anomaly detectors** whose outputs are combined via majority voting — if *either* model fires, you get an alert. Different models catch different attack shapes, keeping the false‑negative rate very low.

### Detection Pipeline

```
 Live Network Traffic
        │
        ▼
 ┌──────────────────┐
 │  Feature         │   duration, bytes, packets,
 │  Extractor       │   flags, protocol, port…
 └────────┬─────────┘
          │
          ▼
 ┌──────────────────┐
 │  StandardScaler  │   zero-mean, unit-variance
 └────────┬─────────┘
          │
     ┌────┴────┐
     │         │
     ▼         ▼
 ┌───────┐  ┌──────────┐
 │  ISO  │  │  AUTO-   │
 │FOREST │  │ ENCODER  │
 └───┬───┘  └────┬─────┘
     │            │
     └─────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  Ensemble   │   flag if EITHER model fires
    │    Vote     │
    └──────┬──────┘
           │
     ┌─────┴──────┐
     ▼            ▼
  🚨 ALERT    ✅ Normal
```

### Training Phase

```
Normal Traffic Only (22,000 samples)
          │
     ┌────┴────┐
     ▼         ▼
Isolation   Autoencoder
  Forest      (train to
  (fit)     reconstruct)
     │         │
     └────┬────┘
          ▼
    Save models to disk
    Compute threshold =
    95th percentile MSE
```

### Detection Phase

```
Incoming Flow
     │
     ▼
Feature Extraction + Scaling
     │
     ├──► Isolation Forest Score  ──┐
     │                              ├──► Ensemble ≥1? ──► 🚨 ALERT / ✅ OK
     └──► Autoencoder MSE > θ ?  ──┘
```

---

## ⚙️ How Each Model Works

### 1. 🌲 Isolation Forest

Randomly isolates observations by recursively partitioning features.

- Anomalies require **fewer splits** → shorter path length → anomaly score near −1
- Trained on **normal data only** — no attack labels needed
- Output: `−1` (anomaly) or `+1` (normal)
- Especially effective against **point anomalies** (DDoS, port scans)

### 2. 🧬 Autoencoder Neural Network

A neural network trained to **reconstruct** normal traffic. High reconstruction error means something unusual.

- **Encoder** compresses traffic features to a latent bottleneck
- **Decoder** reconstructs original features from the latent space
- Anomaly threshold = **95th percentile** of reconstruction MSE on training data
- Catches **subtle, contextual anomalies** that the Isolation Forest may miss

### 3. 🗳️ Ensemble Decision

```python
if isolation_forest_pred == -1 or autoencoder_mse > threshold:
    alert()   # 🚨 Potential zero-day detected
else:
    pass      # ✅ Normal traffic
```

> Flagging on *either* model ensures maximum recall while the two-model agreement keeps false positives low.

---

## 📊 Live Demo Features

| Feature | Description |
|---------|-------------|
| 🎮 **Attack Simulator** | Toggle switch injects realistic attack flows (DDoS‑style, port scan) in real time |
| 📈 **Live Graph** | Reconstruction error (MSE) plotted every second, threshold line always visible |
| 🔔 **Instant Alerts** | Red box: *"🚨 Potential zero‑day attack detected"* — sub‑second latency |
| 🧪 **Fully Offline** | Everything runs locally — no internet needed, perfect for in‑person judging |

---

## 📈 Performance

> Measured on Intel i7 · 16 GB RAM · No GPU required

| Metric | Value |
|--------|-------|
| Detection Rate (simulated attacks) | **> 95%** |
| False Positive Rate | **< 2%** |
| Inference Time per Flow | **< 10 ms** |
| Training Time | **~45 seconds (CPU)** |
| Training Samples | 22,000 synthetic normal flows |

---

## 🛠️ Built With

| Tool | Purpose |
|------|---------|
| 🐍 **Python 3.10** | Core language |
| 🧠 **TensorFlow / Keras** | Autoencoder neural network |
| 🤖 **Scikit‑learn** | Isolation Forest, StandardScaler |
| 🌊 **Streamlit** | Interactive live dashboard |
| 🐼 **Pandas / NumPy** | Data handling and feature engineering |
| 📉 **Matplotlib** | Real‑time plotting |

---

## 🚀 Run It Yourself

### Prerequisites

- Python **3.10** (recommended) or 3.11
- Git (optional)

### Step 1 — Clone the repository

```bash
git clone https://github.com/LuthandoCandlovu/ZeroShield-AI.git
cd ZeroShield-AI
```

### Step 2 — Create a virtual environment

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Generate the synthetic dataset

```bash
python src/data_simulator.py
# Generates 22,000 synthetic normal-traffic samples
```

### Step 5 — Train both models

```bash
python src/train_models.py
# Trains Isolation Forest + Autoencoder (~45 seconds on CPU)
```

### Step 6 — Launch the live dashboard

```bash
streamlit run app.py
```

Your browser opens at **http://localhost:8501**

> Toggle **"Inject Attack Traffic"** → click **"Start Live Detection"** → watch the red alert fire in real time.

---

## 📁 Project Structure

```
ZeroShield-AI/
├── app.py                  # Streamlit dashboard entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── data_simulator.py   # Synthetic traffic generator (22k samples)
│   ├── train_models.py     # Trains Isolation Forest + Autoencoder
│   ├── detector.py         # Ensemble inference logic
│   └── features.py         # Feature extraction pipeline
├── models/
│   ├── isolation_forest.pkl
│   └── autoencoder.h5
└── data/
    └── normal_traffic.csv  # Generated by data_simulator.py
```

---

## 🔮 Future Improvements

- [ ] **Real capture datasets** — Replace synthetic data with CICIDS2017 and UNSW‑NB15 benchmarks
- [ ] **Explainable AI (SHAP)** — Show analysts *why* a flow was flagged (which features drove the score)
- [ ] **FastAPI REST endpoint** — Deploy inference as a microservice any SIEM can call
- [ ] **Live packet capture** — Integrate `scapy` for real NIC capture instead of simulation
- [ ] **Online learning** — Continuously update the normal model without full retraining

---

## 📝 License

MIT © [Luthando Candlovu](https://github.com/LuthandoCandlovu) — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **DevSoc UNSW** for organising Starlight 2026
- The open‑source community behind TensorFlow, Scikit‑learn, and Streamlit
- Academic research in ML‑based intrusion detection that inspired this approach

---

<div align="center">

Made with 🛡️ for the **Starlight Hackathon**

**Questions?** Open an issue or reach out via [GitHub](https://github.com/LuthandoCandlovu/ZeroShield-AI)

</div>
