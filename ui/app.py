import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="FailureMind",
    layout="centered"
)

st.title("🧠 FailureMind")
st.subheader("RAG-based Failure Risk Analyzer")

question = st.text_area(
    "Describe the issue or ask a failure-related question:",
    placeholder="Why do industrial pumps fail under high load?"
)

if st.button("Analyze Risk"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing risk..."):
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=30
            )

        if response.status_code != 200:
            st.error("Backend error. Check FastAPI logs.")
        else:
            data = response.json()

            # 🔴 Risk level
            risk_color = {
                "HIGH": "red",
                "MEDIUM": "orange",
                "LOW": "green"
            }.get(data["risk_level"], "gray")

            st.markdown(
                f"### Risk Level: "
                f"<span style='color:{risk_color}'>{data['risk_level']}</span>",
                unsafe_allow_html=True
            )

            st.metric("Risk Score", data["risk_score"])

            st.markdown("### ⚠️ Likely Failure")
            st.write(data["likely_failure"])

            st.markdown("### 📌 Evidence")
            for e in data.get("evidence", []):
                st.write(f"- {e}")

            st.markdown("### 🛠 Recommended Actions")
            for a in data.get("recommended_actions", []):
                st.write(f"- {a}")
