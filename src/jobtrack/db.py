from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from jobtrack.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url.get_secret_value(),
    echo=settings.debug,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    with SessionLocal() as db:
        yield db
