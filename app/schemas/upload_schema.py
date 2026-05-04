from pydantic import BaseModel


class UploadResponse(BaseModel):
    file_id: str
    file_name: str
    Status: str