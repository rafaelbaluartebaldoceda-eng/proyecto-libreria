"""Infraestructura de conexion y sesiones SQLAlchemy para PostgreSQL."""

import os
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
_ENV_LOADED = False
_ENGINE = None
_SESSION_FACTORY = None


def _load_env_file():
    """Carga variables desde un archivo .env si existe."""
    global _ENV_LOADED
    if _ENV_LOADED or not ENV_FILE.exists():
        _ENV_LOADED = True
        return

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        os.environ.setdefault(key, value)

    _ENV_LOADED = True


def get_db_config():
    """Retorna la configuracion necesaria para conectarse a PostgreSQL."""
    _load_env_file()

    config = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT", "5432"),
    }

    missing = [key for key, value in config.items() if key != "port" and not value]
    if missing:
        raise ValueError(
            "Faltan variables de entorno de base de datos: "
            + ", ".join(sorted(missing))
        )

    try:
        config["port"] = int(config["port"])
    except ValueError as error:
        raise ValueError("DB_PORT debe ser un numero entero valido") from error

    return config


def get_database_url():
    """Construye una URL SQLAlchemy segura a partir de las variables DB_*."""
    config = get_db_config()
    return URL.create(
        "postgresql+psycopg2",
        username=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        database=config["database"],
    )


def get_driver_connect_args():
    """Retorna argumentos explicitos para el driver psycopg2."""
    config = get_db_config()
    return {
        "host": config["host"],
        "database": config["database"],
        "user": config["user"],
        "password": config["password"],
        "port": config["port"],
    }


def get_engine():
    """Retorna el engine SQLAlchemy compartido por toda la aplicacion."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = create_engine(
            "postgresql+psycopg2://",
            connect_args=get_driver_connect_args(),
            future=True,
            pool_pre_ping=True,
        )
    return _ENGINE


def get_connection():
    """Retorna una sesion SQLAlchemy lista para operar sobre la base de datos."""
    global _SESSION_FACTORY
    if _SESSION_FACTORY is None:
        _SESSION_FACTORY = sessionmaker(
            bind=get_engine(),
            class_=Session,
            autoflush=False,
            expire_on_commit=False,
            future=True,
        )
    return _SESSION_FACTORY()


def reset_engine():
    """Reinicia el engine y la factory, util para pruebas o recarga controlada."""
    global _ENGINE, _SESSION_FACTORY
    if _ENGINE is not None:
        _ENGINE.dispose()
    _ENGINE = None
    _SESSION_FACTORY = None


@contextmanager
def managed_connection(connection=None):
    """
    Reutiliza una sesion existente o crea una nueva para una operacion.

    Cuando crea la sesion, se encarga de commit, rollback y cierre.
    """
    if connection is not None:
        yield connection
        return

    session = get_connection()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
