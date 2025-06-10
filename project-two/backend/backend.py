from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
from typing import Dict, Any

"""
LLM Writing Assistant Backend

This FastAPI application serves as the backend for the LLM Writing Assistant.
It provides an endpoint that integrates with a local Ollama-hosted LLM for text improvements.
"""

app = FastAPI(title="LLM Writing Assistant API")

# Allow CORS for integration with the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROMPTS = {
    "grammar": {
        "system": (
            "You are a meticulous English grammar assistant. "
            "ONLY fix grammar, punctuation, and minor style issues. "
            "PRESERVE the original meaning and style. "
            "NEVER add introductory phrases or explanations. "
            "NEVER say 'here is a rewritten version' or similar. "
            "OUTPUT ONLY THE CORRECTED TEXT, NOTHING ELSE. "
        ),
    },
    "full": {
        "system": (
            "You are an expert writing coach. "
            "Improve clarity, coherence, style, and grammar. "
            "NEVER add introductory phrases or explanations. "
            "NEVER say 'here is a rewritten version' or similar. "
            "OUTPUT ONLY THE IMPROVED TEXT, NOTHING ELSE. "
        ),
    },
}


def make_system_prompt(mode: str, weight: str) -> str:
    base_prompt = PROMPTS.get(mode, PROMPTS["full"])["system"]

    if mode == "full":
        weight = weight.lower()
        if weight == "light":
            return base_prompt + (
                " Make only minor corrections, such as fixing grammar, spelling, and punctuation. "
                "Do not rephrase or restructure sentences. Preserve the original voice and style."
            )
        elif weight == "moderate":
            return base_prompt + (
                " Improve grammar, style, and clarity. You may rephrase awkward sentences, "
                "but keep the author's tone and structure mostly intact."
            )
        else:
            return base_prompt + (
                " Revise the text freely to enhance clarity, coherence, and academic tone. "
                "You may rewrite, restructure, or improve the vocabulary as needed, "
                "as long as the original meaning is preserved."
            )

    return base_prompt


async def assist_report(text: str, mode: str = "full", weight: str = "moderate") -> str:
    if not text:
        return ""

    system_prompt = make_system_prompt(mode, weight)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]

    # No timeout for long LLM responses
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            "http://127.0.0.1:11434/v1/chat/completions",
            json={"model": "llama3:8b", "messages": messages}
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


@app.post("/assist")
async def assist_endpoint(request: Request) -> Dict[str, Any]:
    data = await request.json()
    original_text = data.get("text", "")
    mode = data.get("mode", "full")
    weight = data.get("weight", "moderate")

    assisted_text = await assist_report(original_text, mode, weight)
    return {"assisted_text": assisted_text}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
