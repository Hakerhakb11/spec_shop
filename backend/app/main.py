from fastapi import FastAPI

from app.modules.catalog.router import router as catalog_router
from app.modules.users.router import router as users_router

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Spec Shop API. Go to /docs for documentation."}


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "message": "API is running"}


app.include_router(catalog_router)
app.include_router(users_router)
