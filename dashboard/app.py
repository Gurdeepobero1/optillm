import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.metrics import logs

st.title("🚀 OptiLLM Dashboard")

total_cost = sum([log["cost"] for log in logs])
total_requests = len(logs)
cache_hits = len([log for log in logs if log["cached"]])

st.metric("Total Requests", total_requests)
st.metric("Total Cost", f"${total_cost:.4f}")
st.metric("Cache Hits", cache_hits)

st.write("### Logs")

for log in logs:
    st.json(log)