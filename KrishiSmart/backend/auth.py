"""Register / login with simple tokens. Owner: Avijit"""
import hashlib, secrets
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from database import load, save

router = APIRouter(prefix="/api/auth", tags=["auth"])
TOKENS = {}  # token -> user (in memory; cleared when server restarts)


def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()


def ensure_admin():
    users = load("users", [])
    if not any(u["role"] == "admin" for u in users):
        users.append({"id": 1, "name": "Admin", "phone": "admin",
                      "password_hash": hash_pw("admin123"), "role": "admin"})
        save("users", users)


class Register(BaseModel):
    name: str
    phone: str
    password: str


class Login(BaseModel):
    phone: str
    password: str


@router.post("/register")
def register(d: Register):
    users = load("users", [])
    if any(u["phone"] == d.phone for u in users):
        raise HTTPException(400, "This phone number is already registered")
    users.append({"id": max([u["id"] for u in users], default=0) + 1, "name": d.name,
                  "phone": d.phone, "password_hash": hash_pw(d.password), "role": "farmer"})
    save("users", users)
    return {"message": "Registered. Please log in."}


@router.post("/login")
def login(d: Login):
    for u in load("users", []):
        if u["phone"] == d.phone and u["password_hash"] == hash_pw(d.password):
            token = secrets.token_hex(16)
            TOKENS[token] = u
            return {"token": token, "name": u["name"], "role": u["role"]}
    raise HTTPException(401, "Wrong phone or password")


def current_user(authorization: str = Header(default="")):
    user = TOKENS.get(authorization.replace("Bearer ", ""))
    if not user:
        raise HTTPException(401, "Please log in")
    return user


def admin_only(authorization: str = Header(default="")):
    user = current_user(authorization)
    if user["role"] != "admin":
        raise HTTPException(403, "Admin only")
    return user
