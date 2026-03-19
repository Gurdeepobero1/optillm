import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from core.db import SessionLocal, Usage

st.set_page_config(page_title="OptiLLM", layout="wide")

# ---------------- LANDING ----------------
st.title("🚀 OptiLLM")
st.subheader("AI Cost Optimization Layer")

st.markdown("""
Reduce LLM cost and latency using smart caching and routing.

### Features:
- ⚡ Semantic Caching  
- 🧠 Smart Routing  
- 🛟 Fallback Models  
- 📊 Real-time Analytics  
""")

# ---------------- PLAYGROUND ----------------
st.divider()
st.subheader("🧪 API Playground")

api_key = st.text_input("Enter API Key", type="password")
prompt = st.text_area("Enter your prompt")

if st.button("Send Request"):
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        headers={"x-api-key": api_key},
        json={"prompt": prompt}
    )

    data = response.json()

    st.write("### Response")
    st.write(data.get("response"))

    st.write("### Metadata")
    st.json(data)

# ---------------- DASHBOARD ----------------
st.divider()
st.subheader("📊 Usage Dashboard")

db = SessionLocal()
data = db.query(Usage).all()
db.close()

total_requests = len(data)
cache_hits = len([d for d in data if d.cached])
total_cost = sum([d.cost for d in data])

col1, col2, col3 = st.columns(3)

col1.metric("Total Requests", total_requests)
col2.metric("Cache Hits", cache_hits)
col3.metric("Total Cost", f"${round(total_cost,4)}")

# ---------------- COST SAVINGS ----------------
baseline_cost = total_requests * 0.001

if baseline_cost > 0:
    savings = ((baseline_cost - total_cost) / baseline_cost) * 100
else:
    savings = 0

st.success(f"🚀 You saved {round(savings,2)}% cost using OptiLLM")

# ---------------- LOGS ----------------
st.divider()
st.subheader("📜 Recent Requests")

for d in reversed(data[-10:]):
    st.write({
        "query": d.query,
        "latency": round(d.latency, 3),
        "cached": d.cached
    })