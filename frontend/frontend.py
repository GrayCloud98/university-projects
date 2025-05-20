import streamlit as st
import requests
import difflib
from typing import Dict, Any

"""
LLM Writing Assistant

This Streamlit application provides a user interface for the LLM Writing Assistant.
It allows users to input their draft text, select correction options, and view the improved versions.

"""

# Define the backend API URL
API_URL = "http://127.0.0.1:8000"

def send_text_for_assistance(text: str, mode: str, weight: float) -> Dict[str, Any]:
    """
    Send the text to the backend API for assistance.
    
    Parameters:
        text (str): The original seminar report text
        mode (str): The correction mode ("full" or "grammar")
        weight (float): The influence weight for suggestions
    
    Returns:
        Dict containing the API response (including assisted text)
    """
    payload = {
        "text": text,
        "mode": mode,
        "weight": weight
    }
    try:
        response = requests.post(f"{API_URL}/assist", json=payload)
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error connecting to the backend: {e}")
        return {"assisted_text": ""}

def display_diff(original: str, revised: str) -> str:
    """
    Generate a diff view between original and revised text.
    
    This is a simple implementation. Students should enhance this with
    better formatting, color-coding, or a more sophisticated diff library.
    
    Parameters:
        original (str): The original text
        revised (str): The revised text
    
    Returns:
        str: The diff text showing changes
    """
    diff = difflib.ndiff(original.splitlines(), revised.splitlines())
    return "\n".join(diff)

def main():
    """Main application function that sets up the Streamlit UI."""
    st.title("LLM Writing Assistant")
    
    # Input section
    st.subheader("Report Draft")
    original_text = st.text_area("Enter your report draft here:", height=200)
    
    # Controls section
    st.subheader("Assistance Options")
    col1, col2 = st.columns(2)
    
    with col1:
        mode = st.radio(
            "Select correction mode:",
            options=["full", "grammar"],
            index=0,
            help="Full mode improves content and style. Grammar mode only fixes grammar errors."
        )
    
    with col2:
        weight = st.slider(
            "Adjust influence of new suggestions:",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            help="0 = keep original text, 1 = full AI suggestions"
        )
    
    # Process button
    if st.button("Get Assistance"):
        if not original_text:
            st.warning("Please enter some text first.")
            return
            
        with st.spinner("Processing your text..."):
            response = send_text_for_assistance(original_text, mode, weight)
            assisted_text = response.get("assisted_text", "")
        
        # Display results
        if assisted_text:
            st.subheader("Revised Text")
            st.text_area("Revised Seminar Report:", value=assisted_text, height=200)
            
            st.subheader("Differences")
            diff_text = display_diff(original_text, assisted_text)
            st.text_area("Diff Viewer:", value=diff_text, height=200)
            
            # TODO for students: Add a better visual diff display
            st.info("Enhancement opportunity: Implement a colored, side-by-side diff view here!")

if __name__ == "__main__":
    main()