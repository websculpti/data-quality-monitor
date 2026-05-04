from fastapi import APIRouter

from app.utils.logger import get_logger


router = APIRouter()

logger = get_logger(__name__)


@router.get("/health")
def health_check():

    logger.info("Health check endpoint hit")

    return {
        "status": "ok",
        "service": "Data Quality Monitor API",
        "version": "1.0"
    }