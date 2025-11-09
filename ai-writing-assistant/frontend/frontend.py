import streamlit as st
import requests
import difflib
from typing import Dict, Any
import io
from gtts import gTTS

st.set_page_config(page_title="LLM Writing Assistant", layout="wide")
st.markdown(
    """
    <style>
      .stTextArea textarea { min-height: 300px !important; resize: vertical !important; }
    </style>
    """,
    unsafe_allow_html=True
)

API_URL = "http://127.0.0.1:8000"

if "history" not in st.session_state:
    st.session_state.history = []

if "revised_text" not in st.session_state:
    st.session_state.revised_text = ""

if "submitted" not in st.session_state:
    st.session_state.submitted = False


def send_text_for_assistance(text: str, mode: str, weight: str) -> Dict[str, Any]:
    payload = {"text": text, "mode": mode, "weight": weight}
    try:
        response = requests.post(f"{API_URL}/assist", json=payload)
        return response.json()
    except requests.RequestException:
        st.error("Error connecting to the backend.")
        return {"assisted_text": ""}


def display_diff(original: str, revised: str) -> str:
    diff = difflib.ndiff(original.splitlines(), revised.splitlines())
    return "\n".join(diff)


def main():
    st.title("LLM Writing Assistant")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Report Draft")
        original_text = st.text_area("Enter your report draft here:", height=300)

        uploaded = st.file_uploader("Or upload a .txt file:", type=["txt"])

        mode = st.radio("Select correction mode:", ["full", "grammar", "rewrite", "summarize"], horizontal=True)

        if mode == "full":
            weight = st.select_slider("Editing intensity:",
                                      options=["Light", "Moderate", "Heavy"],
                                      value="Moderate")
        elif mode in ["grammar", "rewrite", "summarize"]:
            weight = "Moderate"
            st.select_slider("Editing intensity:",
                             options=["Light", "Moderate", "Heavy"],
                             value=weight,
                             disabled=True)
            st.caption("Editing intensity is only available in 'full' mode.")

        if st.button("Get Assistance"):
            if not original_text.strip() and uploaded:
                original_text = uploaded.read().decode(errors="ignore")

            if not original_text.strip():
                st.warning("Please enter your report text or upload a file.")
                return

            with st.spinner("Processing your text..."):
                response = send_text_for_assistance(original_text, mode, weight)
                st.session_state.revised_text = response.get("assisted_text", "")
                st.session_state.history.append(st.session_state.revised_text)
                st.session_state.submitted = True

    with col2:
        st.subheader("Revised Text")
        st.text_area("Revised Report:",
                     value=st.session_state.revised_text,
                     height=300,
                     label_visibility="hidden")
        if st.session_state.submitted and st.session_state.revised_text:
            mp3 = io.BytesIO()
            gTTS(st.session_state.revised_text).write_to_fp(mp3)
            mp3.seek(0)
            st.audio(mp3, format="audio/mp3")

    if st.session_state.submitted and st.session_state.revised_text:
        st.download_button("Download Revised Text",
                           st.session_state.revised_text,
                           "revised_report.txt",
                           mime="text/plain")
        if uploaded:
            uploaded.seek(0)
            raw = uploaded.read().decode(errors="ignore")
            st.subheader("Uploaded Text")
            st.text_area("", raw, height=150, disabled=True)

        st.subheader("Feedback")

        if "feedback_log" not in st.session_state:
            st.session_state.feedback_log = []

        with st.form("feedback_form"):
            agree = st.radio("Was this revision helpful?", ["👍 Yes", "👎 No"], key="feedback_radio")
            comment = st.text_area("Leave a comment (optional):", key="feedback_input")
            submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            st.session_state.feedback_log.append({
                "useful": agree,
                "comment": comment,
                "text_version": st.session_state.revised_text
            })
            st.success("✅ Feedback submitted!")

        with st.expander("Revision History"):
            for i, version in enumerate(st.session_state.history, 1):
                st.text_area(f"Version {i}", version, height=100)


if __name__ == "__main__":
    main()
