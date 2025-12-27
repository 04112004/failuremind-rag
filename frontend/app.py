import streamlit as st
import requests

st.title("🔥 FailureMind – Pre-Failure Intelligence")

q = st.text_area("Describe your system or ask a risk question")

if st.button("Analyze Risk"):
    res = requests.post(
        "http://localhost:8000/analyze",
        params={"question": q}
    )
    st.json(res.json())
