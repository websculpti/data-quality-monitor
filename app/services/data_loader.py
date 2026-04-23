import uuid
from fastapi import HTTPException, UploadFile
from app.utils.config import DATA_DIR
from app.utils.logger import get_logger
from pathlib import Path
import pandas as pd

logger = get_logger(__name__)


def save_uploaded_file(file: UploadFile):
    if not file.filename.endswith(".csv"):
        logger.error("Invalid file type uploaded")
        raise HTTPException(
            status_code=400,
            detail="Upload csv file only"
        )

    file_id = str(uuid.uuid4())

    file_path = DATA_DIR / f"{file_id}.csv"

    with open(file_path, "wb") as f:
        content = file.file.read()

        if not content:
            logger.error("Empty file uploaded")
            raise HTTPException(
                status_code=400,
                detail="Empty file is uploaded"
            )

        f.write(content)

    logger.info(f"File uploaded successfully: {file.filename}")

    return file_id, str(file_path)


def load_dataset(file_id: str) -> pd.DataFrame:

    file_path = DATA_DIR / f"{file_id}.csv"

    if not file_path.exists():
        logger.error("File not found")
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    try:
        df = pd.read_csv(file_path)

    except Exception:
        logger.error("Failed to parse CSV file")
        raise HTTPException(
            status_code=400,
            detail="Failed to parse CSV file"
        )

    if df.empty:
        logger.error("Dataset is empty")
        raise HTTPException(
            status_code=400,
            detail="Empty dataset"
        )

    logger.info(f"Dataset loaded successfully: {file_path}")

    return df