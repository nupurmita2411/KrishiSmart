# 🌾 KrishiSmart — Crop Disease Detection & Local Farmers Support
CSE451 (Software Engineering), IUB, Autumn 2026.

## Run it (3 commands)
```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```
Open http://127.0.0.1:8000

- Admin login: phone `admin`, password `admin123`
- Farmer: register on the home page, then log in.

## Project structure
| Folder / file | What it is | Owner |
|---|---|---|
| `backend/main.py, database.py, auth.py, diagnosis.py` | API core, login, diagnose, history | Avijit |
| `frontend/index.html, style.css, app.js` | Login/register page, shared style & helpers | Avijit |
| `backend/prices.py`, `backend/data/prices.json`, `frontend/prices.html` | Market price module | Nupur |
| `backend/admin.py`, `frontend/admin.html` | Admin dashboard | Sabbir |
| `ml/predict.py, ml/train_model.py`, `backend/data/diseases.json`, `frontend/diagnose.html, history.html` | AI module + diagnosis pages | Fariha |

## Simplifications (prototype)
- JSON files instead of PostgreSQL (`backend/data/`).
- AI prediction is a **dummy** by default (`ml/predict.py`); the real CNN (`ml/train_model.py`) is plugged in automatically when `ml/model.keras` exists.
- Plain HTML/JS frontend instead of React/Next.js; local folder instead of cloud image storage.
- Bangla interface and Supabase/PostgreSQL are planned as future work.
