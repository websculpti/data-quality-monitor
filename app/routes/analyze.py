from fastapi import APIRouter
from app.utils.logger import get_logger
from app.services.data_loader import load_data
from app.services.data_quality import run_data_quality_checks

logger=get_logger(__name__)

router=APIRouter()

@router.get('/analyze/{file_id}')
def analyze(file_id :str):
    data=load_data(file_id)

    metrics=run_data_quality_checks(data)
    logger.info(f"Analysis Completed for {file_id}")
    return metrics
    # return {'status':'ok'}