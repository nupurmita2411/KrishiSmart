"""KrishiSmart entry point. Owner: Avijit
Run:  cd backend && uvicorn main:app --reload     then open http://127.0.0.1:8000
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import auth, diagnosis, prices, admin
from database import UPLOAD_DIR

app = FastAPI(title="KrishiSmart")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
auth.ensure_admin()

for module in (auth, diagnosis, prices, admin):
    app.include_router(module.router)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
FRONTEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")  # keep LAST
