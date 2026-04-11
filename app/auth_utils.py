"""Utilidades reutilizables para hashing y manejo de JWT."""

import os
from datetime import datetime, timedelta, timezone
from hmac import compare_digest
from pathlib import Path

from jose import jwt
from pwdlib import PasswordHash


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
_ENV_LOADED = False
_PASSWORD_HASH = PasswordHash.recommended()


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
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))

    _ENV_LOADED = True


def get_security_settings():
    """Retorna la configuracion de seguridad necesaria para JWT."""
    _load_env_file()

    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("Falta la variable de entorno SECRET_KEY")

    raw_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    try:
        expire_minutes = int(raw_minutes)
    except ValueError as error:
        raise ValueError(
            "ACCESS_TOKEN_EXPIRE_MINUTES debe ser un numero entero valido"
        ) from error

    if expire_minutes <= 0:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES debe ser mayor que cero")

    return {
        "secret_key": secret_key,
        "algorithm": "HS256",
        "access_token_expire_minutes": expire_minutes,
    }


def get_admin_bootstrap_token() -> str:
    """Retorna el token secreto usado para bootstrap del primer admin."""
    _load_env_file()

    bootstrap_token = os.getenv("ADMIN_BOOTSTRAP_TOKEN")
    if not bootstrap_token:
        raise ValueError("Falta la variable de entorno ADMIN_BOOTSTRAP_TOKEN")
    if bootstrap_token.strip() != bootstrap_token or len(bootstrap_token) < 16:
        raise ValueError(
            "ADMIN_BOOTSTRAP_TOKEN debe tener al menos 16 caracteres y no usar espacios externos"
        )
    return bootstrap_token


def verify_admin_bootstrap_token(provided_token: str) -> bool:
    """Compara en tiempo constante el token recibido con el configurado."""
    if not isinstance(provided_token, str) or not provided_token:
        return False
    expected_token = get_admin_bootstrap_token()
    return compare_digest(provided_token, expected_token)


def hash_password(password: str) -> str:
    """Convierte una contrasena plana en un hash seguro."""
    return _PASSWORD_HASH.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica una contrasena plana contra su hash persistido."""
    return _PASSWORD_HASH.verify(password, hashed_password)


def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    """Genera un JWT firmado a partir del payload recibido."""
    if not isinstance(data, dict):
        raise ValueError("El payload del token debe ser un diccionario.")
    subject = data.get("sub")
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("El token requiere un claim 'sub' valido.")
    if "role" in data and data["role"] not in {"admin", "user"}:
        raise ValueError("El claim 'role' del token es invalido.")

    settings = get_security_settings()
    to_encode = data.copy()
    expire_minutes = (
        expires_minutes
        if expires_minutes is not None
        else settings["access_token_expire_minutes"]
    )
    if not isinstance(expire_minutes, int) or expire_minutes <= 0:
        raise ValueError("La expiracion del token debe ser un entero positivo.")
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings["secret_key"],
        algorithm=settings["algorithm"],
    )


def decode_access_token(token: str) -> dict:
    """Decodifica y valida un JWT firmado por la aplicacion."""
    if not isinstance(token, str) or not token.strip():
        raise ValueError("El token recibido es invalido.")
    settings = get_security_settings()
    return jwt.decode(
        token,
        settings["secret_key"],
        algorithms=[settings["algorithm"]],
    )
