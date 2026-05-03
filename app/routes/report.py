from fastapi import APIRouter, HTTPException
from app.utils.logger import get_logger
from app.services.report_generator import generate_report_with_llm

logger=get_logger(__name__)

router=APIRouter()

@router.get("/report/{file_id}")
def get_report(file_id ):
    logger.info(f"Report generation request for {file_id}")

    result=generate_report_with_llm(file_id)
    logger.info(f"report returned successfully for {file_id}")
    return result