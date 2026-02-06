import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import math

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Shor’s Algorithm vs HTTPS Security",
    layout="wide"
)

st.title("🔐 Quantum Attack on HTTPS using Shor’s Algorithm")
st.caption("A visual, system-level analysis of RSA failure under quantum adversaries")

# =========================================================
# RSA SETUP (DEMO SCALE)
# =========================================================
p, q = 17, 23
n = p * q
phi = (p - 1) * (q - 1)
e = 3
d = pow(e, -1, phi)

session_key = random.randint(20, 80)
encrypted_key = pow(session_key, e, n)

# =========================================================
# SECTION 1 — RSA STRUCTURE
# =========================================================
st.header("RSA Public Key Structure")

df_rsa = pd.DataFrame({
    "Component": ["Prime p", "Prime q", "Public Modulus n"],
    "Value": [p, q, n]
})

fig_rsa = px.bar(
    df_rsa,
    x="Component",
    y="Value",
    text_auto=True,
    title="RSA Key Composition",
    template="plotly_dark"
)
st.plotly_chart(fig_rsa, use_container_width=True)

# ---------------- FLOW STRIP ----------------
st.markdown("### 🔁 HTTPS Key Exchange Flow")
cols = st.columns(5)
labels = [
    "Client\n(Browser)",
    "RSA Public Key",
    "Encrypted\nSession Key",
    "Private Key",
    "AES Channel"
]
for col, label in zip(cols, labels):
    col.info(label)

# =========================================================
# SECTION 2 — FACTORING DIFFICULTY
# =========================================================
st.header("Factoring Difficulty Comparison")

df_time = pd.DataFrame({
    "Method": ["Classical Computer", "Quantum Computer (Shor)"],
    "Time (log scale)": [1e9, 1e2]
})

fig_time = px.bar(
    df_time,
    x="Method",
    y="Time (log scale)",
    log_y=True,
    text_auto=True,
    title="Time to Factor RSA Modulus",
    template="plotly_dark"
)
st.plotly_chart(fig_time, use_container_width=True)

# ---------------- METRICS PANEL ----------------
st.markdown("### 📊 Cryptographic State Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("RSA Modulus (n)", n)
c2.metric("Key Exchange", "RSA")
c3.metric("Quantum Threat Level", "HIGH", delta="↑")
c4.metric("Data Longevity Risk", "SEVERE")

# =========================================================
# SECTION 3 — SECURITY DEGRADATION
# =========================================================
st.header("Long-Term Security Degradation")

st.progress(75)
st.caption("Encrypted traffic recorded today becomes vulnerable once quantum capability matures")

# =========================================================
# SECTION 4 — ATTACK TIMELINE
# =========================================================
st.header("Store-Now → Decrypt-Later Attack Timeline")

timeline_df = pd.DataFrame({
    "Stage": [
        "HTTPS Session",
        "Traffic Recorded",
        "Quantum Computer Exists",
        "Shor’s Algorithm Executed",
        "Private Key Recovered",
        "Data Decrypted"
    ],
    "Time Index": [0, 1, 4, 5, 6, 7]
})

fig_timeline = px.scatter(
    timeline_df,
    x="Time Index",
    y="Stage",
    size=[30]*6,
    title="Quantum Threat Timeline",
    template="plotly_dark"
)
fig_timeline.update_traces(marker=dict(color="red"))
st.plotly_chart(fig_timeline, use_container_width=True)



# =========================================================
# SECTION 5 — SHOR’S ATTACK
# =========================================================
st.header("Quantum Factorization (Simulated Shor’s Algorithm)")

if st.button("Run Shor’s Algorithm"):
    p_found, q_found = p, q
    d_eve = pow(e, -1, (p_found - 1) * (q_found - 1))
    recovered_key = pow(encrypted_key, d_eve, n)

    c1, c2, c3 = st.columns(3)
    c1.metric("Recovered p", p_found)
    c2.metric("Recovered q", q_found)
    c3.metric("Recovered Session Key", recovered_key)

# =========================================================
# SECTION 6 — CASCADE FAILURE
# =========================================================
st.header("Cascading Cryptographic Failure")

cols = st.columns(3)
cols[0].error("RSA Private Key\nCompromised")
cols[1].warning("Session Key\nExposed")
cols[2].success("AES Data\nReadable")

# =========================================================
# SECTION 7 — RSA vs QKD
# =========================================================
st.header("Why QKD Stops This Attack")

radar_df = pd.DataFrame({
    "Property": [
        "Future-Safe",
        "Store-Now Attack Resistant",
        "Relies on Math",
        "Eavesdrop Detection",
        "Long-Term Confidentiality"
    ],
    "RSA": [0, 0, 1, 0, 0],
    "QKD": [1, 1, 0, 1, 1]
})

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=radar_df["RSA"],
    theta=radar_df["Property"],
    fill="toself",
    name="RSA"
))

fig_radar.add_trace(go.Scatterpolar(
    r=radar_df["QKD"],
    theta=radar_df["Property"],
    fill="toself",
    name="QKD"
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(range=[0, 1])),
    title="Security Model Comparison",
    template="plotly_dark"
)

st.plotly_chart(fig_radar, use_container_width=True)

# =========================================================
# FINAL VERDICT
# =========================================================
st.markdown("### 🛡️ Security Verdict")

st.success("""
• RSA enables delayed compromise under quantum adversaries  
• AES remains secure but depends on key exchange  
• Shor’s algorithm breaks RSA retrospectively  
• QKD removes the mathematical attack surface entirely
""")
