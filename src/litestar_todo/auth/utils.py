from datetime import datetime, timedelta
from uuid import UUID

from os import environ
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr

from litestar_todo.auth.models import User
from litestar_todo.auth.repositories import UserRepository
from litestar import Litestar, Request, Response, get, post
from litestar.connection import ASGIConnection
from litestar.openapi.config import OpenAPIConfig
from litestar.security.jwt import JWTAuth, Token

import jwt
from litestar.exceptions import NotAuthorizedException
from pydantic import UUID4, BaseModel

from litestar_todo.main.config import settings

DEFAULT_TIME_DELTA = timedelta(days=1)
ALGORITHM = settings.JWT_ALGORITHM


class TokenSchema(BaseModel):
    exp: datetime
    iat: datetime
    sub: UUID4


def decode_jwt_token(encoded_token: str) -> TokenSchema:
    """Decode a JWT token and return the value stored under the ``sub`` key.

    If the token is invalid or expired (i.e. the value stored under the ``exp`` key
    is in the past), an exception is raised.
    """
    try:
        payload = jwt.decode(jwt=encoded_token, key=settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return TokenSchema(**payload)
    except jwt.PyJWTError as e:
        raise NotAuthorizedException("Invalid token") from e


def encode_jwt_token(user_id: UUID, expiration: timedelta = DEFAULT_TIME_DELTA) -> str:
    """Encode a JWT token with expiration and a given user_id."""
    token = TokenSchema(
        exp=datetime.now() + expiration,
        iat=datetime.now(),
        sub=user_id,
    )
    return jwt.encode(token.model_dump(), settings.JWT_SECRET_KEY, algorithm=ALGORITHM)


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    """Retrieve the user from the database using the token."""
    # Decode the token to get the user ID
    decoded_token = decode_jwt_token(encoded_token=token)
    user_id = decoded_token.sub

    rep = UserRepository()
    user = await rep.get_user_by_id(user_id=user_id)
    if user:
        return user
    return None


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.JWT_SECRET_KEY,
    exclude=["/docs", "/auth/login", "/auth/register"],
)
