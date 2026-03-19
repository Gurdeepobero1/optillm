import sys
import os

# ✅ FIX PATH (CRITICAL)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import time
import uuid

from core.llm import query_llm
from core.cache import search_cache, add_to_cache
from core.router import select_model
from core.db import SessionLocal, Usage, User, init_db

init_db()

st.set_page_config(page_title="OptiLLM", layout="wide")

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- AUTH ----------
def create_user(name):
    db = SessionLocal()
    user = User(name=name, api_key=str(uuid.uuid4()))
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

def regenerate_key(user):
    db = SessionLocal()
    user.api_key = str(uuid.uuid4())
    db.commit()
    db.close()

# ---------- LOGIN ----------
if not st.session_state.user:
    st.title("🔐 Welcome to OptiLLM")

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
        new_name = st.text_input("Create Username")
        if st.button("Signup"):
            if new_name:
                user = create_user(new_name)
                st.session_state.user = user
                st.success(f"API Key: {user.api_key}")
                st.rerun()
            else:
                st.error("Enter username")

    st.stop()

user = st.session_state.user

# ---------- SIDEBAR ----------
st.sidebar.title("👤 Account")
st.sidebar.write(user.name)
st.sidebar.code(user.api_key)

if st.sidebar.button("🔄 Regenerate Key"):
    regenerate_key(user)
    st.rerun()

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ---------- MAIN ----------
st.title("🚀 OptiLLM")

prompt = st.text_area("Enter prompt")

if st.button("Run Query"):
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
        answer = query_llm(prompt)
        latency = time.time() - start

        add_to_cache(prompt, answer)

        st.success("✅ Response")
        st.write(answer)

        db = SessionLocal()
        db.add(Usage(user_id=user.id, query=prompt, latency=latency, cost=0.001, cached=False))
        db.commit()
        db.close()

# ---------- METRICS ----------
db = SessionLocal()
data = db.query(Usage).all()
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
st.success(f"🚀 {round(savings,2)}% cost saved")

# ---------- LOGS ----------
st.subheader("📜 Logs")

for d in reversed(data[-5:]):
    st.write({
        "query": d.query,
        "latency": round(d.latency, 3),
        "cached": d.cached
    })