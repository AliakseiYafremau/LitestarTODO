from __future__ import annotations

from typing import TYPE_CHECKING

from litestar_todo.auth.dto import UserReadScheme
from litestar_todo.auth.models import User

if TYPE_CHECKING:
    from litestar_todo.auth.repositories import UserRepository


class UserService:
    """Service class for user-related operations.

    Provides CRUD operations for user management using UserRepository.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """Initialize the UserService with a UserRepository instance.

        Args:
            user_repository: The repository instance for database operations.

        """
        self.user_repository = user_repository

    async def get_by_id(self, user_id: str) -> UserReadScheme | None:
        """Retrieve a single user by its ID.

        Args:
            user_id: The UUID of the user to retrieve.

        Returns:
            UserReadDTO if the user exists, None otherwise.

        """
        exist = await self.user_repository.exists(id=user_id)
        if not exist:
            return None
        db_user = await self.user_repository.get(item_id=user_id)
        return UserReadScheme(id=db_user.id, username=db_user.username)

    async def get_by_username(self, username: str) -> UserReadScheme | None:
        """Retrieve a single user by its username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            UserReadDTO if the user exists, None otherwise.

        """
        exist = await self.user_repository.exists(username=username)
        if not exist:
            return None
        db_user = await self.user_repository.get_one(username=username)
        return UserReadScheme(id=db_user.id, username=db_user.username)

    async def get_all(self) -> list[UserReadScheme]:
        """Retrieve all users.

        Returns:
            A list of UserReadScheme objects representing all users.
            Returns empty list if no users exist.

        """
        all_users = await self.user_repository.list()
        if all_users:
            return [
                UserReadScheme(
                    id=element.id,
                    username=element.username,
                )
                for element in all_users
            ]
        return []

    async def create(
        self,
        username: str,
        password: str,
    ) -> UserReadScheme:
        """Create a new user.

        Args:
            username: The username of the new user.
            password: The password of the new user.

        Returns:
            UserReadScheme object representing the created user.

        """
        db_user = await self.user_repository.add(
            data=User(username=username, password=password),
            auto_commit=True,
        )
        return UserReadScheme(id=db_user.id, username=db_user.username)

    async def delete(self, user_id: str) -> UserReadScheme:
        """Delete a user.

        Args:
            user_id: The UUID of the user to delete.

        Returns:
            UserReadScheme object representing the deleted user.

        """
        db_user = await self.user_repository.delete(item_id=user_id)
        return UserReadScheme(id=db_user.id, username=db_user.username)


async def provide_user_service(
    user_repository: UserRepository,
) -> UserService:
    """Provide a UserService instance.

    Args:
        user_repository: The repository instance for database operations.

    Returns:
        An instance of UserService.

    """
    return UserService(user_repository=user_repository)
