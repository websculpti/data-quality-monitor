from pydantic import BaseModel

class ReportContent(BaseModel):
    summary: str
    risk_level: str
    recommendations: str


class ReportResponse(BaseModel):
    file_id: str
    report: ReportContent
    report_path: str