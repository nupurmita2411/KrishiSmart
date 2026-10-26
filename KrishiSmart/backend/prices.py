"""Public market price API (search by crop and market). Owner: Nupur"""
from fastapi import APIRouter
from database import load

router = APIRouter(prefix="/api/prices", tags=["prices"])


@router.get("")
def list_prices(crop: str = "", market: str = ""):
    rows = load("prices", [])
    if crop:
        rows = [r for r in rows if crop.lower() in r["crop"].lower()]
    if market:
        rows = [r for r in rows if market.lower() in r["market"].lower()]
    return sorted(rows, key=lambda r: r["date"], reverse=True)


@router.get("/meta")
def meta():
    rows = load("prices", [])
    return {"crops": sorted({r["crop"] for r in rows}),
            "markets": sorted({r["market"] for r in rows})}
