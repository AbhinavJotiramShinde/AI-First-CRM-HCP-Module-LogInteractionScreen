from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json

from app.ai.langgraph_agent import agent
from app.db.session import get_db
from app.db.models import Interaction

router = APIRouter(prefix="/chat", tags=["AI"])


class ChatRequest(BaseModel):
    message: str


@router.post("")
def chat_ai(payload: ChatRequest):
    """
    Only runs AI and returns structured JSON
    """
    try:
        result = agent.invoke({"input": payload.message})
        raw_output = result["output"]

        if isinstance(raw_output, dict):
            parsed = raw_output
        else:
            parsed = json.loads(raw_output)

        return parsed

    except Exception as e:
        print("❌ AI Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/and-save")
def chat_and_save(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Runs AI → Parses → Saves into DB → Returns saved row
    """
    try:
        # 1️⃣ Run AI
        result = agent.invoke({"input": payload.message})
        raw_output = result["output"]

        if isinstance(raw_output, dict):
            parsed = raw_output
        else:
            parsed = json.loads(raw_output)

        # 2️⃣ Save to DB
        interaction = Interaction(
            hcp_name=parsed.get("hcp_name"),
            topics=json.dumps(parsed.get("topics", [])),
            sentiment=parsed.get("sentiment"),
            materials_shared=json.dumps(parsed.get("materials_shared", [])),
            samples_distributed=parsed.get("samples_distributed", 0),
            outcomes=json.dumps(parsed.get("outcomes", [])),
            follow_ups=json.dumps(parsed.get("follow_ups", [])),
        )

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return {
            "message": "AI extracted & saved successfully",
            "interaction": interaction
        }

    except Exception as e:
        print("❌ AI → DB Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
