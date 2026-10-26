"""Admin APIs: manage prices, diseases/remedies, users. Owner: Sabbir"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import load, save
from auth import admin_only

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(admin_only)])


class PriceIn(BaseModel):
    crop: str
    market: str
    price_per_kg: float
    date: str  # YYYY-MM-DD


class DiseaseIn(BaseModel):
    id: str
    crop: str
    name: str
    symptoms: str
    remedy: str


# ---- prices ----
@router.post("/prices")
def add_price(p: PriceIn):
    rows = load("prices", [])
    row = {"id": max([r["id"] for r in rows], default=0) + 1, **p.dict()}
    rows.append(row)
    save("prices", rows)
    return row


@router.put("/prices/{price_id}")
def update_price(price_id: int, p: PriceIn):
    rows = load("prices", [])
    for r in rows:
        if r["id"] == price_id:
            r.update(p.dict())
            save("prices", rows)
            return r
    raise HTTPException(404, "Price not found")


@router.delete("/prices/{price_id}")
def delete_price(price_id: int):
    rows = [r for r in load("prices", []) if r["id"] != price_id]
    save("prices", rows)
    return {"message": "Deleted"}


# ---- diseases ----
@router.get("/diseases")
def list_diseases():
    return load("diseases", [])


@router.post("/diseases")
def add_or_update_disease(d: DiseaseIn):
    rows = load("diseases", [])
    for r in rows:
        if r["id"] == d.id:
            r.update(d.dict())
            save("diseases", rows)
            return r
    rows.append(d.dict())
    save("diseases", rows)
    return d


# ---- users ----
@router.get("/users")
def list_users():
    return [{k: v for k, v in u.items() if k != "password_hash"} for u in load("users", [])]


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    users = load("users", [])
    target = next((u for u in users if u["id"] == user_id), None)
    if not target:
        raise HTTPException(404, "User not found")
    if target["role"] == "admin":
        raise HTTPException(400, "Cannot delete admin")
    save("users", [u for u in users if u["id"] != user_id])
    return {"message": "Deleted"}
