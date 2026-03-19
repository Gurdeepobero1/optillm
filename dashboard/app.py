import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from core.db import SessionLocal, Usage

st.set_page_config(page_title="OptiLLM", layout="wide")

# ----------- CUSTOM CSS (PREMIUM LOOK) -----------
st.markdown("""
<style>
.card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.4);
}
.big-text {
    font-size: 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.title("🚀 OptiLLM")
st.caption("AI Cost Optimization Layer")

st.markdown("""
<div class="card">
<b>Reduce LLM Cost & Latency</b><br>
Smart routing + caching + fallback system for AI apps.
</div>
""", unsafe_allow_html=True)

# ----------- PLAYGROUND -----------
st.subheader("🧪 Playground")

api_key = st.text_input("API Key", type="password")
prompt = st.text_area("Enter your prompt")

if st.button("Run Query"):
    with st.spinner("Processing... ⚡"):
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            headers={"x-api-key": api_key},
            json={"prompt": prompt}
        )
        data = response.json()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### Response")
    st.write(data.get("response"))
    st.markdown('</div>', unsafe_allow_html=True)

    st.json(data)

# ----------- METRICS -----------
st.subheader("📊 Metrics")

db = SessionLocal()
data = db.query(Usage).all()
db.close()

total_requests = len(data)
cache_hits = len([d for d in data if d.cached])
total_cost = sum([d.cost for d in data])

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card"><div class="big-text">📈 {total_requests}</div>Total Requests</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card"><div class="big-text">⚡ {cache_hits}</div>Cache Hits</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card"><div class="big-text">💰 ${round(total_cost,4)}</div>Total Cost</div>', unsafe_allow_html=True)

# ----------- COST SAVINGS -----------
baseline_cost = total_requests * 0.001

if baseline_cost > 0:
    savings = ((baseline_cost - total_cost) / baseline_cost) * 100
else:
    savings = 0

st.markdown(f"""
<div class="card">
🚀 <b>You saved {round(savings,2)}% cost</b> using OptiLLM
</div>
""", unsafe_allow_html=True)

# ----------- LOGS -----------
st.subheader("📜 Recent Requests")

for d in reversed(data[-5:]):
    st.markdown(f"""
    <div class="card">
    <b>Query:</b> {d.query}<br>
    <b>Latency:</b> {round(d.latency,3)} sec<br>
    <b>Cached:</b> {d.cached}
    </div>
    """, unsafe_allow_html=True)