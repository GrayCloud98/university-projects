# LLM Writing Assistant

## Overview

This project is a full-stack writing assistant powered by a locally hosted large language model (LLM). The assistant helps users improve their text drafts by offering grammar corrections, full stylistic revisions, rewriting, or summarization.

The backend is built with FastAPI and connects to an LLM running via Ollama. The frontend is implemented in Streamlit and offers an interactive interface for uploading drafts, selecting editing modes, viewing differences, and downloading results. Features include a diff viewer, revision history, and text-to-speech support.

### Technology Stack

- **Backend**: FastAPI  
- **Frontend**: Streamlit  
- **Local LLM**: Ollama (using `llama3:8b`)

---

## 🧠 Ollama Setup (Windows)

1. [Download and install Ollama](https://ollama.com/download)

2. After installation, a black terminal window will open automatically.

3. In that terminal, type the following to download the required model:

```bash
ollama pull llama3:8b
```

---

## 🚀 How to Run the App

Open your IDE terminal (in the root of the project), then run:

```bash
# Create virtual environment in the current folder
python -m venv .venv
```

**Activate the environment:**

On **Windows**:
```bash
.venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the **backend server**:
```bash
python backend/backend.py
```

---

Open a **second terminal**, make sure you're in the root project folder, then:

**Activate the virtual environment again:**

On **Windows**:
```bash
.venv\Scripts\activate
```

Start the **frontend app**:
```bash
streamlit run frontend/frontend.py
```
