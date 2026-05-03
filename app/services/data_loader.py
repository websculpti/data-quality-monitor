import uuid
from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel,Field
from app.utils.config import DATA_DIR
from app.utils.logger import get_logger
from pathlib import Path
import pandas as pd
logger=get_logger(__name__)


def save_uploaded_file(file: UploadFile):
    if not file.filename.endswith('.csv'):
        logger.error(f"Invalid file type uloaded" )
        raise HTTPException(status_code=400,detail="Only CSV files are allowed")
    
    file_id=str(uuid.uuid4())
    file_path=DATA_DIR / f"{file_id}.csv"

    with open(file_path,"wb") as f:
        content=file.file.read()
        if not content:
            logger.error(f"Uploaded file is empty")
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        f.write(content)

    logger.info(f"File uploaded successfully: {file.filename} ")
    
    return file_id, str(file_path)

def load_data(file_id: str):
    file_path=Path(DATA_DIR / f"{file_id}.csv")

    if not file_path.exists():
        logger.error(f"Dataset not found: {file_path}")
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df=pd.read_csv(file_path)
    except Exception:
        logger.error(f"Invalid CSV file")
        raise HTTPException(status_code=400,detail="Invalid CSV file")
    
    if df.empty:
        logger.error(f"CSV file is empty")
        raise HTTPException(status_code=400, detail="CSV file is empty")
    
    logger.info(f"File loaded successfully: {file_path}")
    return df
    