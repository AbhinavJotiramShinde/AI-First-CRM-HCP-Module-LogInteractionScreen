from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_ai import router as ai_router
from app.api.routes_interactions import router as interactions_router
from app.db.session import engine
from app.db.base import Base

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM - HCP Module")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "AI-CRM Backend Running"}

app.include_router(ai_router)
app.include_router(interactions_router)
