"""Endpoints HTTP para autenticacion, registro y perfil del usuario actual."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth_utils import create_access_token, verify_admin_bootstrap_token
from app.dependencies import get_auth_service
from app.schemas.auth import TokenResponse
from app.schemas.usuario import (
    AdminBootstrapRequest,
    UsuarioCreate,
    UsuarioRegister,
    UsuarioResponse,
)
from app.security import get_current_user, require_admin
from services.auth_service import AuthService


router = APIRouter(tags=["Auth"])


@router.post(
    "/auth/bootstrap-admin",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def bootstrap_admin(
    user: AdminBootstrapRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Crea el primer administrador usando un token de bootstrap de un solo proposito."""
    if auth_service.existe_admin_activo():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario administrador activo.",
        )

    try:
        bootstrap_valid = verify_admin_bootstrap_token(user.bootstrap_token)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

    if not bootstrap_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bootstrap token invalido",
        )

    try:
        return auth_service.registrar_usuario(
            user.username,
            str(user.email),
            user.password,
            role="admin",
        )
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_409_CONFLICT
            if "Ya existe" in detail
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error


@router.post(
    "/auth/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UsuarioRegister,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Registra un usuario comun con rol user."""
    try:
        return auth_service.registrar_usuario(
            user.username,
            str(user.email),
            user.password,
            role="user",
        )
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_409_CONFLICT
            if "Ya existe" in detail
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error


@router.post(
    "/auth/users",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_as_admin(
    user: UsuarioCreate,
    admin_user: Annotated[object, Depends(require_admin)],
    auth_service: AuthService = Depends(get_auth_service),
):
    """Permite a un administrador crear usuarios con rol explicito."""
    _ = admin_user
    try:
        return auth_service.registrar_usuario(
            user.username,
            str(user.email),
            user.password,
            role=user.role,
        )
    except ValueError as error:
        detail = str(error)
        status_code = (
            status.HTTP_409_CONFLICT
            if "Ya existe" in detail
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail) from error


@router.post("/token", response_model=TokenResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
):
    """Autentica un usuario y retorna un access token Bearer."""
    user = auth_service.autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        {
            "sub": user.username,
            "role": user.role,
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/users/me", response_model=UsuarioResponse)
def read_users_me(current_user: Annotated[object, Depends(get_current_user)]):
    """Retorna el perfil del usuario autenticado."""
    return current_user
