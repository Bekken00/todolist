from sqlalchemy import create_engine

from app.core.config import settings


engine = create_engine(url=settings.DATABASE_URL(), echo=True)

def init_db() -> None:
    from app.models import Base

    Base.metadata.create_all(engine)

init_db()