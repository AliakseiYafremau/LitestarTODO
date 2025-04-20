from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from litestar.security.jwt import JWTAuth, Token

from litestar_todo.auth.models import User
from litestar_todo.auth.services import provide_auth_service
from litestar_todo.core.database import sqlalchemy_config
from litestar_todo.main.config import settings

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection[Any, Any, Any, Any],
) -> User | None:
    """Retrieve a user instance based on the provided JWT token.

    Parameters
    ----------
    token : Token
        The JWT token containing user information.
    connection : ASGIConnection[Any, Any, Any, Any]
        The ASGI connection object.

    Returns
    -------
    User | None
        The user instance if found, otherwise None.

    """
    session = sqlalchemy_config.provide_session(
        connection.app.state, connection.scope,
    )
    service = await provide_auth_service(session)
    user = await service.get_user(user_id=UUID(token.sub))
    return user if user else None


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.JWT_SECRET_KEY,
    exclude=["/login", "/docs"],
)
