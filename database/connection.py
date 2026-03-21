import os
from contextlib import contextmanager
from pathlib import Path

import psycopg2


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
_ENV_LOADED = False


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


def get_connection():
    """Retorna una conexion activa a la base de datos PostgreSQL."""
    config = get_db_config()
    return psycopg2.connect(
        host=config["host"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
        port=config["port"],
    )


@contextmanager
def managed_connection(connection=None):
    """
    Reutiliza una conexion existente o crea una nueva para una operacion.

    Cuando crea la conexion, se encarga de commit, rollback y cierre.
    """
    if connection is not None:
        yield connection
        return

    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
