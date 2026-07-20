import streamlit as st
from agents.secure_agent import run_agent
from firewall.audit_logger import get_logs

st.set_page_config(layout="wide")
st.title("🛡️ Intent-Drift Firewall Dashboard")

col1, col2 = st.columns([1, 1])

with col1:
    user_task = st.text_area("User Task (e.g., 'Summarize this email')")
    injected_email = st.text_area("Content to Process (e.g., Email body with prompt injection)")
    if st.button("Run Agent"):
        # This calls your core logic
        result = run_agent(user_task, injected_email)
        st.write("Result:", result)

with col2:
    st.subheader("Live Firewall Logs")
    logs = get_logs() # Fetch from your SQLite audit_logger
    st.json(logs)