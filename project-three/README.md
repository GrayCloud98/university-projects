## How to Run the Project

### 1. Create and Activate a Virtual Environment

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies Install Dependencies Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
python backend/backend.py
```

### 4. Start the Frontend App

(In a new terminal, with the virtual environment activated)

```bash
streamlit run frontend/frontend.py
```
