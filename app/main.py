from fastapi import FastAPI

app = FastAPI(
    title="Data Quality Monitor API",
    version="1.0"
)


@app.get("/")
def root():
    return {"message": "Data Quality Monitor running"}


@app.get("/health")
def health():
    return {"status": "ok"}