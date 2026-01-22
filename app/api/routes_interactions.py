from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Interaction
import json

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.post("/")
def save_interaction(data: dict, db: Session = Depends(get_db)):
    interaction = Interaction(
        hcp_name = data.get("hcp_name", ""),
        sentiment = data.get("sentiment", "Neutral"),
        topics = json.dumps(data.get("topics", [])),
        materials_shared = json.dumps(data.get("materials_shared", [])),
        samples_distributed = data.get("samples_distributed", 0),
        outcomes = json.dumps(data.get("outcomes", [])),
        follow_ups = json.dumps(data.get("follow_ups", []))
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("/")
def get_interactions(db: Session = Depends(get_db)):
    try:
        return db.query(Interaction).all()
    except Exception as e:
        print("🔥 ERROR in /interactions:", e)
        raise HTTPException(status_code=500, detail=str(e))
