from fastapi import APIRouter, UploadFile, HTTPException, File
from app.services.data_loader import save_uploaded_file
from app.utils.logger import get_logger


logger = get_logger(__name__)

router = APIRouter()

@router.post("/upload")

def upload_file(file: UploadFile = File(...)):

    file_id, file_path = save_uploaded_file(file)

    logger.info("Dataset uploaded !", file_id)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "status": "uploaded"
    }