from core.llm import query_llm
from core.cache import search_cache, add_to_cache
from core.router import select_model
from core.auth import get_user
from core.db import SessionLocal, Usage
import time
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

    user = get_user(api_key)

    if not user:
        st.error("Invalid API Key")

    else:
        start = time.time()

        cached = search_cache(prompt)

        if cached:
            latency = time.time() - start

            st.success("⚡ Cache Hit")
            st.write(cached)

            db = SessionLocal()
            db.add(Usage(
                user_id=user.id,
                query=prompt,
                latency=latency,
                cost=0,
                cached=True
            ))
            db.commit()
            db.close()

        else:
            with st.spinner("Processing... ⚡"):
                model = select_model(prompt)
                answer = query_llm(prompt)

            latency = time.time() - start

            if "Error" not in answer:
                add_to_cache(prompt, answer)

            st.success("✅ Response")
            st.write(answer)

            db = SessionLocal()
            db.add(Usage(
                user_id=user.id,
                query=prompt,
                latency=latency,
                cost=0.001,
                cached=False
            ))
            db.commit()
            db.close()

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