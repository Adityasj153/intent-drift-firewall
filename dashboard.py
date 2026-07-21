import streamlit as st

from core.context import Context
from core.pipeline import Pipeline


# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Intent Drift Firewall",
    page_icon="🛡️",
    layout="wide"
)


# -------------------------------
# Header
# -------------------------------
st.title("🛡️ Intent Drift Firewall")
st.subheader("AI Security Middleware")
st.write(
    "Analyze user queries for **Intent Drift**, **Prompt Injection**, "
    "risk score, policy decision, and execution results."
)

st.divider()


# -------------------------------
# User Input
# -------------------------------
query = st.text_area(
    "Enter User Query",
    placeholder="Example: What is 25 * 12?",
    height=150
)


# -------------------------------
# Analyze Button
# -------------------------------
if st.button("Analyze Query", type="primary"):

    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    pipeline = Pipeline()
    context = Context(query)

    context = pipeline.run(context)

    st.success("Analysis Complete")

    st.divider()

    col1, col2 = st.columns(2)

    # ----------------------------------
    # Security Analysis
    # ----------------------------------
    with col1:

        st.subheader("🛡️ Security Analysis")

        st.write("**Selected Tool**")
        st.code(context.selected_tool)

        st.write("**Intent Drift**")
        st.json(context.drift)

        st.write("**Prompt Injection**")
        st.json(context.prompt_injection)

        st.write("**Risk Assessment**")
        st.json(context.risk)

        st.write("**Policy Decision**")
        st.json(context.policy)

    # ----------------------------------
    # Execution Details
    # ----------------------------------
    with col2:

        st.subheader("⚙️ Execution")

        st.write("**Execution Metadata**")
        st.json(context.execution)

        st.write("**Result**")
        st.code(str(context.result))

    st.divider()

    # ----------------------------------
    # Full Context
    # ----------------------------------
    with st.expander("📄 Complete Pipeline Context"):

        st.json(context.to_dict())