from __future__ import annotations

from typing import TYPE_CHECKING

from litestar_todo.todo.dto import ListReadDTO, ListScheme
from litestar_todo.todo.models import List
from litestar_todo.todo.repositories import ListRepository

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession


class ListService:
    """Service for managing todo lists.

    Provides CRUD operations for todo lists using ListRepository.
    """

    def __init__(self, list_repo: ListRepository) -> None:
        """Initialize the ListService with a ListRepository instance.

        Args:
            list_repo: The repository instance for database operations.

        """
        self.list_repo = list_repo

    async def get_by_id(self, list_id: UUID) -> ListReadDTO | None:
        """Retrieve a single todo list by its ID.

        Args:
            list_id: The UUID of the list to retrieve.

        Returns:
            ListReadDTO if the list exists, None otherwise.

        """
        exist = await self.list_repo.exists(id=list_id)
        if not exist:
            return None
        db_list = await self.list_repo.get(item_id=list_id)
        return ListScheme(id=db_list.id, title=db_list.title)

    async def get_all(self) -> list[ListReadDTO]:
        """Retrieve all todo lists.

        Returns:
            A list of ListReadDTO objects representing all todo lists.
            Returns empty list if no lists exist.

        """
        all_lists = await self.list_repo.list()
        if all_lists:
            return [
                ListScheme(id=element.id, title=element.title) for element in all_lists
            ]
        return []

    async def create(self, title: str) -> ListReadDTO:
        """Create a new todo list.

        Args:
            title: The title of the new list.

        Returns:
            ListReadDTO representing the newly created list.

        """
        db_list = await self.list_repo.add(data=List(title=title), auto_commit=True)
        return ListScheme(id=db_list.id, title=db_list.title)

    async def delete(self, list_id: UUID) -> ListReadDTO:
        """Delete a todo list.

        Args:
            list_id: The UUID of the list to delete.

        Returns:
            ListReadDTO representing the deleted list.

        """
        db_list = await self.list_repo.delete(item_id=list_id, auto_commit=True)
        return ListScheme(id=db_list.id, title=db_list.title)


async def provide_list_service(db_session: AsyncSession) -> ListService:
    """Dependency provider for ListService.

    Args:
        db_session: AsyncSession for database operations.

    Returns:
        An instance of ListService configured with a ListRepository.

    """
    return ListService(ListRepository(session=db_session))
