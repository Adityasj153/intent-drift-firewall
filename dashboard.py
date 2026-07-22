import streamlit as st
import pandas as pd

from core.context import Context
from core.pipeline import Pipeline
from database.database import Database


# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Intent Drift Firewall",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================================
# Database
# ==========================================================
db = Database()

metrics = db.fetch_metrics()
history = db.fetch_recent_requests(limit=10)


# ==========================================================
# Header
# ==========================================================
st.title("🛡️ Intent Drift Firewall")

st.caption("Production-Ready AI Security Middleware")

st.write(
    """
Analyze user queries through a complete AI security pipeline:

- Tool Routing
- Query Normalization
- Intent Extraction
- Intent Drift Detection
- Prompt Injection Detection
- Risk Assessment
- Policy Decision
- Tool Execution
- Audit Logging
"""
)

st.divider()


# ==========================================================
# Dashboard Metrics
# ==========================================================
st.subheader("📊 Security Overview")

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric(
    "Requests",
    metrics["total"]
)

m2.metric(
    "Allowed",
    metrics["allowed"]
)

m3.metric(
    "Blocked",
    metrics["blocked"]
)

m4.metric(
    "Avg Risk",
    metrics["avg_risk"]
)

m5.metric(
    "Avg Latency",
    f"{metrics['avg_latency']} ms"
)

st.divider()


# ==========================================================
# User Input
# ==========================================================
st.subheader("📝 Analyze Query")

query = st.text_area(
    "Enter User Query",
    placeholder="Example: What is 25 * 12?",
    height=150
)

analyze = st.button(
    "Analyze Query",
    type="primary",
    use_container_width=True
)


# ==========================================================
# Pipeline Execution
# ==========================================================
if analyze:

    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    pipeline = Pipeline()

    context = Context(query)

    with st.spinner("Running Security Pipeline..."):

        context = pipeline.run(context)

    st.success("Analysis Complete")

    st.divider()

    left, right = st.columns(2)

    # ======================================================
    # Security Analysis
    # ======================================================
    with left:

        st.subheader("🛡️ Security Analysis")

        st.markdown("### Selected Tool")
        st.code(context.selected_tool)

        st.markdown("### Intent Drift")
        st.json(context.drift)

        st.markdown("### Prompt Injection")
        st.json(context.prompt_injection)

        st.markdown("### Risk Assessment")
        st.json(context.risk)

        st.markdown("### Policy Decision")
        st.json(context.policy)

    # ======================================================
    # Execution Details
    # ======================================================
    with right:

        st.subheader("⚙️ Execution")

        st.markdown("### Execution Metadata")
        st.json(context.execution)

        st.markdown("### Result")

        if context.result is not None:
            st.code(str(context.result))
        else:
            st.info("No result returned.")

    st.divider()

    # ======================================================
    # Complete Context
    # ======================================================
    with st.expander("📄 Complete Pipeline Context"):

        st.json(context.to_dict())


# ==========================================================
# Request History
# ==========================================================
st.divider()

st.subheader("📜 Recent Requests")

if history:

    df = pd.DataFrame(history)

    preferred_columns = [

        "timestamp",

        "query",

        "selected_tool",

        "risk_score",

        "severity",

        "policy",

        "execution_time",

        "status"

    ]

    columns = [
        c for c in preferred_columns
        if c in df.columns
    ]

    st.dataframe(
        df[columns],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No requests have been logged yet.")