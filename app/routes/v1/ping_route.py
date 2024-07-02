from fastapi import APIRouter

from app.schemas.base_schema import Message

router = APIRouter(prefix="/ping", tags=["Ping"])


@router.get("", response_model=Message)
async def ping():
    return Message(detail="Pong")
