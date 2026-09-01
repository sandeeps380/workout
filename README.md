# Workout Tracker

A small workout tracker built while learning Python, FastAPI, and CI/CD.

- **Backend** (`backend/`): a FastAPI app backed by SQLite (via SQLAlchemy) that exposes
  endpoints for logging and listing workouts.
- **Frontend** (`frontend/`): a static HTML page that talks to the backend API.

## Running the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at
`http://127.0.0.1:8000/docs`.

## Running the frontend

Open `frontend/index.html` directly in a browser, or serve it with any static file server.
