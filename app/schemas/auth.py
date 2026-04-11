"""Schemas Pydantic relacionados con autenticacion."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Representa la respuesta HTTP al autenticarse correctamente."""

    access_token: str
    token_type: str
