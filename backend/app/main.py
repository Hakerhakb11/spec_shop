from fastapi import FastAPI

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Spec Shop API. Go to /docs for documentation."}


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "message": "API is running"}
