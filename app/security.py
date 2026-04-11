"""Dependencias de seguridad y autorizacion basadas en JWT."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.auth_utils import decode_access_token
from app.dependencies import get_auth_service
from services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudo validar el token",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Retorna el usuario autenticado a partir del token Bearer."""
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError as error:
        raise credentials_exception from error

    user = auth_service.obtener_usuario_por_username(username)
    if user is None or not user.activo:
        raise credentials_exception
    return user


def require_admin(current_user: Annotated[object, Depends(get_current_user)]):
    """Permite el acceso solo a usuarios con rol admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a esta ruta",
        )
    return current_user
