"""AIOPS-X Dashboard — Streamlit UI."""
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="AIOPS-X", layout="wide")
st.title("AIOPS-X Dashboard")

API_URL = st.secrets.get("api_url", "http://localhost:8000") if hasattr(st, "secrets") else "http://localhost:8000"

tab1, tab2, tab3 = st.tabs(["Overview", "Events", "Approvals"])

with tab1:
    st.header("System Metrics")
    try:
        metrics = requests.get(f"{API_URL}/metrics").json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Cycles Total", metrics.get("cycles_total", 0))
        col2.metric("Events Detected", metrics.get("events_detected", 0))
        col3.metric("Approvals Pending", requests.get(f"{API_URL}/approvals/pending").json().__len__())
        col1, col2 = st.columns(2)
        col1.metric("Diagnoses Made", metrics.get("diagnoses_made", 0))
        col2.metric("Actions Executed", metrics.get("actions_executed", 0))
    except Exception as e:
        st.error(f"Cannot reach API: {e}")

with tab2:
    st.header("Recent Events")
    try:
        events = requests.get(f"{API_URL}/events?limit=20").json()
        for ev in events:
            st.write(f"**{ev['type']}** at {ev['timestamp']}: {ev['payload']}")
    except Exception as e:
        st.error(str(e))

with tab3:
    st.header("Pending Approvals")
    try:
        pending = requests.get(f"{API_URL}/approvals/pending").json()
        if not pending:
            st.success("No pending approvals")
        for appr in pending:
            with st.expander(f"Tool: {appr['tool']} (requested {appr['created_at']})"):
                st.json(appr)
                col1, col2 = st.columns(2)
                if col1.button("Approve", key=f"appr_{appr['approval_id']}"):
                    requests.post(f"{API_URL}/approvals/{appr['approval_id']}/approve", headers={"X-User-ID": "ui"})
                    st.rerun()
                if col2.button("Reject", key=f"rej_{appr['approval_id']}"):
                    requests.post(f"{API_URL}/approvals/{appr['approval_id']}/reject", headers={"X-User-ID": "ui"})
                    st.rerun()
    except Exception as e:
        st.error(str(e))

st.sidebar.write("AIOPS-X v1.0.0")
st.sidebar.write("Built with GSD")
