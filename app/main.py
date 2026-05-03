from fastapi import FastAPI

#from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.analyze import router as analyze_router
from app.routes.report import router as report_router

from app.utils.logger import get_logger

logger = get_logger(__name__)


app = FastAPI(
    title="Data Quality Monitor API",
    version="1.0",
    description="API for monitoring structured data quality"
)


# Register routes

#app.include_router(health_router)
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(report_router)




@app.on_event("startup")
def startup_event():
    logger.info("Data Quality Monitor API started successfully")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Data Quality Monitor API shutting down")