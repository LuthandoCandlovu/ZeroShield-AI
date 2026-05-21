import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from src.realtime_detector import ZeroShieldDetector

st.set_page_config(page_title="ZeroShield AI", layout="wide")
st.title("🛡️ ZeroShield AI: Real-Time Threat Detection")
st.markdown("Detects **zero‑day cyberattacks** using Isolation Forest + Autoencoder")

# Load detector
@st.cache_resource
def load_detector():
    return ZeroShieldDetector()

detector = load_detector()

# --- Simulated network flow generators ---
def generate_normal_flow():
    return {
        'duration': np.random.exponential(0.05),
        'src_bytes': np.random.normal(200, 50),
        'dst_bytes': np.random.normal(300, 80),
        'packet_rate': np.random.normal(50, 10),
        'syn_flag': np.random.binomial(1, 0.3),
        'ack_flag': np.random.binomial(1, 0.7)
    }

def generate_attack_flow():
    return {
        'duration': np.random.exponential(2),
        'src_bytes': np.random.normal(5000, 1000),
        'dst_bytes': np.random.normal(10, 20),
        'packet_rate': np.random.normal(200, 50),
        'syn_flag': np.random.binomial(1, 0.9),
        'ack_flag': np.random.binomial(1, 0.1)
    }

# Sidebar controls
st.sidebar.header("Attack Simulator")
attack_mode = st.sidebar.checkbox("🔴 Inject Attack Traffic", value=False)
duration = st.sidebar.slider("Demo duration (seconds)", 10, 60, 30)

# Placeholders
placeholder = st.empty()
alert_placeholder = st.empty()
metric_placeholder = st.empty()

# Data storage
history = []
alert_count = 0

# Run demo
if st.sidebar.button("Start Live Detection"):
    st.sidebar.info("Running...")
    start_time = time.time()
    while time.time() - start_time < duration:
        # Generate a flow
        if attack_mode:
            flow = generate_attack_flow()
        else:
            flow = generate_normal_flow()

        # Convert to DataFrame
        df_flow = pd.DataFrame([flow])
        features = df_flow[['duration','src_bytes','dst_bytes','packet_rate','syn_flag','ack_flag']].values

        # Predict
        pred, mse, iso = detector.predict(features)
        is_attack = bool(pred[0])

        # Record
        history.append({
            'time': time.time() - start_time,
            'attack_detected': is_attack,
            'mse': mse[0],
            'iso_anomaly': iso[0],
            'actual_attack': attack_mode
        })

        if is_attack:
            alert_count += 1
            alert_placeholder.error(f"🚨 ALERT: Potential zero‑day attack detected! (Ensemble)")
        else:
            alert_placeholder.success("✅ Traffic appears normal")

        # Show metrics
        metric_placeholder.metric("Alerts so far", alert_count)

        # Update graph
        if len(history) > 1:
            df_hist = pd.DataFrame(history)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df_hist['time'], df_hist['mse'], label='Reconstruction Error (MSE)', color='blue')
            ax.axhline(y=detector.ae_threshold, color='red', linestyle='--', label='Autoencoder Threshold')
            attack_times = df_hist[df_hist['attack_detected'] == True]['time']
            ax.scatter(attack_times, [detector.ae_threshold]*len(attack_times), color='red', marker='x', s=100, label='Attack Alert')
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('MSE')
            ax.set_title('Real‑time Anomaly Score')
            ax.legend()
            ax.grid(True)
            placeholder.pyplot(fig)
            plt.close(fig)

        time.sleep(1)  # one flow per second

    st.success("Demo finished. Refresh to run again.")
