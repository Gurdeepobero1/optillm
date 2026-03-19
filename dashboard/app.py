import streamlit as st
from core.db import SessionLocal, Usage

st.set_page_config(page_title="OptiLLM", layout="wide")

st.title("🚀 OptiLLM")
st.subheader("LLM Optimization & Cost Intelligence Platform")

# --- Fetch Data ---
db = SessionLocal()
data = db.query(Usage).all()
db.close()

total_requests = len(data)
cache_hits = len([d for d in data if d.cached])
total_cost = sum([d.cost for d in data])

col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Requests", total_requests)
col2.metric("⚡ Cache Hits", cache_hits)
col3.metric("💰 Total Cost", f"${round(total_cost,4)}")

# --- Logs ---
st.divider()
st.subheader("📜 Request Logs")
st.sidebar.title("🔧 Controls")
api_key = st.sidebar.text_input("API Key", type="password")

query = st.sidebar.text_area("Enter Prompt")

if st.sidebar.button("Send"):
    st.write("Coming next: API playground")

for d in reversed(data[-10:]):
    st.container().write({
        "query": d.query,
        "latency": round(d.latency, 3),
        "cached": d.cached
    })