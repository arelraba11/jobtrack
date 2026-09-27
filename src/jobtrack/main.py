from fastapi import FastAPI

from jobtrack.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
