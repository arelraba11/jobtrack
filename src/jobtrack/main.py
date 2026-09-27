from fastapi import FastAPI

from jobtrack.config import get_settings
from jobtrack.routers import companies

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(companies.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
