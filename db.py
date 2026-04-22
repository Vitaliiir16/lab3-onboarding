from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, scoped_session
from config import Config

config = Config()


class Base(DeclarativeBase):
    pass


def ensure_database_exists():
    """Create the database if it does not exist."""
    engine = create_engine(config.database_url_without_db, echo=False)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{config.DB_NAME}` "
                          f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.commit()
    engine.dispose()


engine = create_engine(config.database_url, echo=False)

session_factory = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

ScopedSession = scoped_session(session_factory)


def get_session() -> Session:
    """Get a new database session."""
    return ScopedSession()


def init_db():
    """Create all tables in the database."""
    ensure_database_exists()

    global engine, session_factory, ScopedSession
    engine = create_engine(config.database_url, echo=False)
    session_factory = sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    ScopedSession = scoped_session(session_factory)

    # Import models so they register with Base.metadata
    import models.employee  # noqa: F401
    import models.equipment  # noqa: F401
    import models.account  # noqa: F401

    Base.metadata.create_all(engine)
