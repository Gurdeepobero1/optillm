import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import time
import uuid

from core.llm import query_llm
from core.cache import search_cache, add_to_cache
from core.db import SessionLocal, Usage, User, init_db

init_db()

st.set_page_config(page_title="OptiLLM", layout="wide")

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- AUTH ----------
def create_user(name, api_key):
    db = SessionLocal()
    user = User(name=name, api_key=api_key)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def get_user(name):
    db = SessionLocal()
    user = db.query(User).filter(User.name == name).first()
    db.close()
    return user

# ---------- LOGIN ----------
if not st.session_state.user:
    st.title("🔐 OptiLLM Login")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        name = st.text_input("Username")

        if st.button("Login"):
            user = get_user(name)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("User not found")

    with tab2:
        new_name = st.text_input("Username")
        user_api_key = st.text_input("Your Sarvam API Key", type="password")

        if st.button("Signup"):
            if new_name and user_api_key:
                user = create_user(new_name, user_api_key)
                st.session_state.user = user
                st.success("Account created")
                st.rerun()
            else:
                st.error("Fill all fields")

    st.stop()

user = st.session_state.user

# ---------- SIDEBAR ----------
st.sidebar.title("👤 Account")
st.sidebar.write(user.name)

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ---------- MAIN ----------
st.title("🚀 OptiLLM")

prompt = st.text_area("Enter your prompt")

if st.button("Run Query"):

    if not user.api_key:
        st.error("❌ API key missing. Please login again.")
        st.stop()

    start = time.time()

    cached = search_cache(prompt)

    if cached:
        latency = time.time() - start

        st.success("⚡ Cache Hit")
        st.write(cached)

        db = SessionLocal()
        db.add(Usage(user_id=user.id, query=prompt, latency=latency, cost=0, cached=True))
        db.commit()
        db.close()

    else:
        with st.spinner("Calling AI..."):
            answer = query_llm(prompt, user.api_key)

        if answer.startswith("❌"):
            st.error(answer)
            st.stop()

        latency = time.time() - start

        add_to_cache(prompt, answer)

        st.success("✅ Response")
        st.write(answer)

        # cost estimation
        cost = len(prompt) * 0.00001

        db = SessionLocal()
        db.add(Usage(user_id=user.id, query=prompt, latency=latency, cost=cost, cached=False))
        db.commit()
        db.close()

# ---------- METRICS ----------
db = SessionLocal()
data = db.query(Usage).filter(Usage.user_id == user.id).all()
db.close()

st.subheader("📊 Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Requests", len(data))
col2.metric("Cache Hits", len([d for d in data if d.cached]))
col3.metric("Cost", f"${round(sum(d.cost for d in data),4)}")

# ---------- SAVINGS ----------
baseline = len(data) * 0.001
actual = sum(d.cost for d in data)

savings = ((baseline - actual) / baseline * 100) if baseline else 0
st.success(f"🚀 Cost Saved: {round(savings,2)}%")

# ---------- LOGS ----------
st.subheader("📜 Activity")

for d in reversed(data[-5:]):
    st.write({
        "query": d.query,
        "latency": round(d.latency, 3),
        "cached": d.cached
    })