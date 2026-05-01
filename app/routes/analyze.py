from fastapi import APIRouter
from app.services.data_loader import load_dataset
from app.services.data_quality import run_data_quality_checks
from app.utils.logger import get_logger

# creating router that will generate analysis of the dataset using run data quality checks

router = APIRouter()

logger = get_logger(__name__)

@router.get("/analyze/{file_id}")
def analyze(file_id: str):

    data = load_dataset(file_id)
    metrics = run_data_quality_checks(data)

    logger.info("Analysis completed for dataset: %s", file_id)

    return metrics