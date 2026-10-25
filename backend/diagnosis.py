"""Upload leaf photo -> AI model -> result + history. Owner: Avijit"""
import os, sys, uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from database import load, save, UPLOAD_DIR
from auth import current_user

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml"))
from predict import predict  # written by Fariha (ml/predict.py)

router = APIRouter(prefix="/api", tags=["diagnosis"])
ALLOWED = {"image/jpeg": ".jpg", "image/png": ".png"}
MAX_BYTES = 5 * 1024 * 1024
THRESHOLD = 0.60  # below this -> "not sure, ask an expert" (Figure 3)


@router.post("/diagnose")
async def diagnose(file: UploadFile = File(...), user=Depends(current_user)):
    if file.content_type not in ALLOWED:
        raise HTTPException(400, "Only JPG or PNG photos are allowed")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(400, "Photo is too large (max 5 MB)")

    filename = uuid.uuid4().hex + ALLOWED[file.content_type]
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(data)

    result = predict(path)  # {"disease_id": "...", "confidence": 0.87}
    disease = next((d for d in load("diseases", []) if d["id"] == result["disease_id"]), None)
    sure = result["confidence"] >= THRESHOLD

    history = load("diagnoses", [])
    record = {
        "id": max([h["id"] for h in history], default=0) + 1,
        "user_id": user["id"],
        "image_url": "/uploads/" + filename,
        "crop": disease["crop"] if disease else "Unknown",
        "disease_name": disease["name"] if disease else "Unknown",
        "symptoms": disease["symptoms"] if disease else "",
        "remedy": disease["remedy"] if disease else "",
        "disease_name_bn": disease.get("name_bn", disease["name"]) if disease else "অজানা",
        "symptoms_bn": disease.get("symptoms_bn", disease["symptoms"]) if disease else "",
        "remedy_bn": disease.get("remedy_bn", disease["remedy"]) if disease else "",
        "confidence": round(result["confidence"], 2),
        "sure": sure,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    history.append(record)
    save("diagnoses", history)
    return record


@router.get("/history")
def history(user=Depends(current_user)):
    rows = [h for h in load("diagnoses", []) if h["user_id"] == user["id"]]
    return list(reversed(rows))
