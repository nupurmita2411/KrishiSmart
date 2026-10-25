"""Tiny JSON-file 'database' (dummy replacement for PostgreSQL). Owner: Avijit"""
import json, os, threading

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
UPLOAD_DIR = os.path.join(BASE, "uploads")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
_lock = threading.Lock()


def load(name, default):
    path = os.path.join(DATA_DIR, name + ".json")
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with _lock:
        with open(os.path.join(DATA_DIR, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
