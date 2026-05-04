from fastapi import APIRouter
from app.utils.logger import get_logger
from app.services.data_loader import load_data
from app.services.data_quality import run_data_quality_checks
from app.schemas.analyze_schema import AnalyzeResponse

logger=get_logger(__name__)

router=APIRouter()

@router.post('/analyze/{file_id}', response_model=AnalyzeResponse)
def analyze(file_id :str):
    data=load_data(file_id)

    metrics=run_data_quality_checks(data)
    logger.info(f"Analysis Completed for {file_id}")
    return metrics
    # return {'status':'ok'}