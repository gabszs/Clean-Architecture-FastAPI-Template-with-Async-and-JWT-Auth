from fastapi import APIRouter

from app.core.telemetry import logger
from app.schemas.base_schema import Message

router = APIRouter(prefix="/healthcheck", tags=["Health"])


@router.get("", response_model=Message)
async def ping():
    logger.info("Healthcheck triggered successfully")
    return Message(detail="Success")
