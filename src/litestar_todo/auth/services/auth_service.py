from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Callable

import jwt
from litestar.response import (
    Response,  # Adjust the import path based on your project structure
)
from litestar.status_codes import HTTP_400_BAD_REQUEST
from sqlalchemy.ext.asyncio import AsyncSession

from litestar_todo.auth.dto import UserCreateScheme, UserReadScheme, UserScheme
from litestar_todo.auth.models import User
from litestar_todo.auth.repositories import UserRepository

if TYPE_CHECKING:
    from uuid import UUID

    from litestar import Request
    from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    """Service class for authentication-related operations.

    Provides methods for user authentication and token generation.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        """Initialize the AuthService with a UserRepository instance.

        Args:
            user_repository: Repository for user-related operations.

        """
        self.user_repository = user_repository

    async def authenticate(self, data: UserCreateScheme) -> UserReadScheme | None:
        """Authenticate a user by username and password.

        Args:
            data: UserCreateScheme containing username and password.

        Returns:
            UserReadScheme if authentication is successful, None otherwise.

        """
        user = await self.get_user(username=data.username)
        if not user or not await self.verify_password(data.password, user.password):
            return None  # Должно вызывать исключение
        return UserReadScheme(id=user.id, username=user.username)  # Тут тоже

    async def get_user(self, username: str) -> UserScheme | None:
        """Retrieve a user by username.

        Args:
            username: The username of the user.

        Returns:
            UserScheme if the user exists, None otherwise.

        """
        exist = await self.user_repository.exists(username=username)
        if not exist:
            return None
        db_user = await self.user_repository.get_one(username=username)
        return UserScheme(
            id=db_user.id,
            username=db_user.username,
            password=db_user.password,
        )

    async def generate_token(self, user_id: UUID, secret: str, algorithm: str) -> str:
        """Generate a token for the authenticated user.

        Args:
            user_id: The UUID of the user.
            secret: The secret key used for token generation.
            algorithm: The algorithm to use for token generation.

        Returns:
            A token string for the authenticated user.

        """
        payload = {"user_id": str(user_id)}
        return jwt.encode(payload, secret, algorithm=algorithm)

    async def hash_password(self, password: str) -> str:
        """Hash a user's password.

        Args:
            password: The plain text password to be hashed.

        Returns:
            The hashed password.

        """
        return password  # Just to give an example

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a user's password against the stored hashed password.

        Args:
            plain_password: The plain text password provided by the user.
            hashed_password: The hashed password stored in the database.

        Returns:
            True if the password matches, False otherwise.

        """
        return plain_password == hashed_password  # Just to give an example

    async def register(self, data: UserCreateScheme) -> UserReadScheme:
        """Register a new user.

        Args:
            data: UserCreateScheme containing username and password.

        Returns:
            UserReadScheme for the newly created user.

        Raises:
            ValueError: If the username is already taken.

        """
        exist = await self.user_repository.exists(username=data.username)
        if exist:
            raise ValueError("Username is already taken.")

        hashed_password = await self.hash_password(data.password)
        new_user = await self.user_repository.add(
            data=User(
                username=data.username,
                password=hashed_password,
            ),
            auto_commit=True,
        )
        return UserReadScheme(id=new_user.id, username=new_user.username)

    async def verify_token(self, token: str, secret: str, algorithm: str) -> UserReadScheme | None:
        """Verify the validity of a token and return the associated user.

        Args:
            token: The token to verify.
            secret: The secret key used for token verification.
            algorithm: The algorithm used for token verification.

        Returns:
            UserReadScheme if the token is valid, None otherwise.

        """
        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])
            user_id = payload.get("user_id")
            if not user_id:
                return None

            user = await self.user_repository.get(item_id=user_id)
            if not user:
                return None

            return UserReadScheme(id=user.id, username=user.username)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


async def provide_auth_service(db_session: AsyncSession) -> AuthService:
    """Provide an instance of AuthService.

    Args:
        db_session: Database session for user-related operations.

    Returns:
        An instance of AuthService.

    """
    return AuthService(UserRepository(session=db_session))
