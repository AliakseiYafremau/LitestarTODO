from __future__ import annotations

from typing import TYPE_CHECKING

from litestar_todo.auth.models import User
from litestar_todo.auth.repositories import UserRepository

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    """Service for handling authentication-related operations.

    This service provides methods to retrieve users and create new users
    by interacting with the UserRepository.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """Initialize the AuthService with a UserRepository.

        Args:
            user_repository: An instance of UserRepository to interact with user data.

        """
        self.user_repository = user_repository

    async def get_user(self, user_id: UUID) -> User | None:
        """Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            User instance if found, None otherwise.

        """
        result = await self.user_repository.exists(id=user_id)
        if result:
            return await self.user_repository.get_one(id=user_id)
        return None

    async def create_user(self, username: str, password: str) -> User:
        """Create a new user.

        Args:
            username: The username of the user to create.
            password: The password of the user to create.

        Returns:
            The created User instance.

        """
        user = User(username=username, password=password)
        await self.user_repository.add(user, auto_commit=True)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        """Retrieve a user by their username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            User instance if found, None otherwise.

        """
        result = await self.user_repository.exists(username=username)
        if result:
            return await self.user_repository.get_one(username=username)
        return None


async def provide_auth_service(db_session: AsyncSession) -> AuthService:
    """Provide an instance of AuthService.

    Args:
        db_session: The database session to be used by the repository.

    Returns:
        An instance of AuthService.

    """
    return AuthService(UserRepository(session=db_session))
