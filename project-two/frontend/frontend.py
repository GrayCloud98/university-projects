import streamlit as st
import requests
import difflib
from typing import Dict, Any
import io
from gtts import gTTS
import streamlit.components.v1 as components

st.set_page_config(page_title="LLM Writing Assistant", layout="wide")
st.markdown(
    """
    <style>
      .stTextArea textarea { min-height: 300px !important; resize: vertical !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the backend API URL
API_URL = "http://127.0.0.1:8000"

# Initialize revision history
if "history" not in st.session_state:
    st.session_state.history = []


def send_text_for_assistance(text: str, mode: str, weight: float) -> Dict[str, Any]:
    """
    Send the text to the backend API for assistance.
    """
    payload = {"text": text, "mode": mode, "weight": weight}
    try:
        response = requests.post(f"{API_URL}/assist", json=payload)
        return response.json()
    except requests.RequestException:
        st.error("Error connecting to the backend.")
        return {"assisted_text": ""}


def display_diff(original: str, revised: str) -> str:
    """
    Generate a simple diff view between original and revised text.
    """
    diff = difflib.ndiff(original.splitlines(), revised.splitlines())
    return "\n".join(diff)


def main():
    # App title
    st.title("LLM Writing Assistant")

    col1, col2 = st.columns(2)

    with col1:
        # Input text area
        st.subheader("Report Draft")
        original_text = st.text_area("Enter your report draft here:", height=300)
        st.button("🎤", key="mic_button")
        # Correction mode selector
        mode = st.radio(
            "Select correction mode:",
            ["full", "grammar"],
            horizontal=True
        )

        # Influence slider
        weight = st.slider(
            "Adjust influence of new suggestions:",
            0.0,
            1.0,
            0.5
        )

        # File uploader
        uploaded = st.file_uploader(
            "Upload a .txt file to compare:",
            type=["txt"]
        )

        # Button to trigger assistance
        get_btn = st.button("Get Assistance")

    with col2:
        # Placeholder for the revised text
        st.subheader("Revised Text")
        revised_placeholder = st.empty()
        revised_placeholder.text_area("Revised Report:", value="", height=300, label_visibility="hidden")
        st.button("🔊", key="speaker_button")

    # Process on button click
    if get_btn:
        if not original_text.strip() and uploaded:
            original_text = uploaded.read().decode(errors="ignore")

        if not original_text.strip():
            st.warning("Please enter your report text.")
            return

        with st.spinner("Processing your text..."):
            response = send_text_for_assistance(original_text, mode, weight)
            assisted_text = response.get("assisted_text", "")

        # Display revised text
        revised_placeholder.text_area(
            "Revised Seminar Report:",
            value=assisted_text,
            height=300,
            label_visibility="hidden"
        )

        # Download button for revised text
        st.download_button(
            "Download Revised Text",
            assisted_text,
            "revised_report.txt",
            mime="text/plain"
        )

        # Text-to-speech playback of revised text
        mp3 = io.BytesIO()
        gTTS(assisted_text).write_to_fp(mp3)
        mp3.seek(0)
        st.audio(mp3, format="audio/mp3")

        # Copy to clipboard button
        components.html(
            f"<button onclick=\"navigator.clipboard.writeText(`{assisted_text}`);\">Copy to Clipboard</button>",
            height=30
        )

        # Compare with uploaded file
        if uploaded:
            raw = uploaded.read().decode(errors="ignore")
            st.subheader("Uploaded Text")
            st.text_area("", raw, height=150, label_visibility="hidden")
            st.subheader("Diff with Uploaded File")
            st.text_area("", display_diff(raw, assisted_text), height=150, label_visibility="hidden")

        # Display plain diff
        st.subheader("Differences")
        st.text_area(
            "Diff Viewer:",
            display_diff(original_text, assisted_text),
            height=200
        )

        # Feedback section
        agree = st.radio(
            "Was this revision helpful?",
            ["👍 Yes", "👎 No"],
            key="feedback_radio"
        )
        comment = st.text_input(
            "Any feedback?",
            key="feedback_input"
        )
        if st.button("Submit Feedback"):
            st.success("Thanks for your feedback!")

        # Append to revision history
        st.session_state.history.append(assisted_text)
        with st.expander("Revision History"):
            for i, version in enumerate(st.session_state.history, 1):
                st.text_area(
                    f"Version {i}",
                    version,
                    height=100
                )


if __name__ == "__main__":
    main()
