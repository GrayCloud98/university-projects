from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any

"""
LLM Writing Assistant Backend

This FastAPI application serves as the backend for the LLM Writing Assistant.
It provides an endpoint that simulates LLM-based text improvements and corrections.

Students are expected to expand this template by:
1. Implementing actual Ollama integration
2. Enhancing the text processing logic
3. Adding additional endpoints as needed
"""

app = FastAPI(title="LLM Writing Assistant API")

# Allow CORS for integration with the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def assist_report(text: str, mode: str = "full", weight: float = 0.5) -> str:
    """
    Simulate LLM-based assistance for report editing.
    
    This is a placeholder function. Students should replace this with actual
    Ollama integration to provide real text improvements.
    
    Parameters:
        text (str): The original text to be improved
        mode (str): Either "full" for comprehensive improvements or "grammar" for grammar-only corrections
        weight (float): A value between 0.0 and 1.0 that determines how much the suggestions influence the result
                        0.0 = original text only, 1.0 = fully revised text
    
    Returns:
        str: The assisted/improved text
    """
    if not text:
        return ""
        
    # This is just a placeholder implementation
    if mode == "grammar":
        # In a real implementation, this would only fix grammar issues
        grammar_corrections = f"Grammar-corrected: {text}"
        # Simulate applying the weight between original and corrected text
        return text if weight < 0.1 else grammar_corrections
    else:
        # In a real implementation, this would do a comprehensive revision
        full_revision = f"Completely revised: {text}"
        # Simulate applying the weight between original and revised text
        if weight < 0.3:
            return text
        elif weight < 0.7:
            return f"Partially improved: {text}"
        else:
            return full_revision

@app.post("/assist")
async def assist_endpoint(request: Request) -> Dict[str, Any]:
    """
    API endpoint that accepts a seminar report draft and returns an improved version.
    
    Expects a JSON payload with:
    - text: The original seminar report text
    - mode: The correction mode ("full" or "grammar")
    - weight: A float value between 0.0 and 1.0 determining the influence of suggestions
    
    Returns:
        Dict containing the assisted text
    """
    data = await request.json()
    original_text = data.get("text", "")
    mode = data.get("mode", "full")
    weight = data.get("weight", 0.5)
    
    # Process the text with the assist_report function
    assisted_text = assist_report(original_text, mode, weight)
    
    return {"assisted_text": assisted_text}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)