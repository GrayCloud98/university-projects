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

### 3. Navigate to backend folder

```bash
uvicorn main:app --reload
```

### 4. Start the Frontend App

(In a new terminal, with the virtual environment activated, go to frontend folder)

```bash
streamlit run app.py
```
