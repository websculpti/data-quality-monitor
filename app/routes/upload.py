from fastapi import APIRouter, UploadFile, File, HTTPException,FastAPI
from app.services.data_loader import save_uploaded_file
from app.utils.logger import get_logger
from app.utils.config import DATA_DIR
from app.schemas.upload_schema import UploadResponse
logger=get_logger(__name__)

router=APIRouter()
"""
This endpoint allows users to upload a csv file and save it and returns fild_id(as in job_id) and file path.
It uses a service fucntion called save_uploaded_file to handle all this.
"""
@router.post("/upload", response_model=UploadResponse)
def upload_csv(file: UploadFile = File(...)):
    file_id, file_path = save_uploaded_file(file)
    logger.info(f"File uploaded and saved: {file_id}")
    return {
        "file_id": file_id,
        "file_name": file.filename,
        "Status": "Uploaded"
    }