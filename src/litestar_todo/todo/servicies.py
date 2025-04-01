from __future__ import annotations

from typing import TYPE_CHECKING

from litestar_todo.todo.dto import ListReadDTO, ListScheme, NoteReadDTO, NoteScheme
from litestar_todo.todo.models import List, Note
from litestar_todo.todo.repositories import ListRepository, NoteRepository

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


class NoteService:
    """Service for managing todo notes.

    Provides CRUD operations for todo notes using NoteRepository.
    """

    def __init__(self, note_repo: NoteRepository) -> None:
        """Initialize the NoteService with a NoteRepository instance.

        Args:
            note_repo: The repository instance for database operations.

        """
        self.note_repo = note_repo

    async def get_by_id(self, note_id: UUID) -> NoteReadDTO | None:
        """Retrieve a single todo note by its ID.

        Args:
            note_id: The UUID of the note to retrieve.

        Returns:
            NoteReadDTO if the note exists, None otherwise.

        """
        exist = await self.note_repo.exists(id=note_id)
        if not exist:
            return None
        db_note = await self.note_repo.get(item_id=note_id)
        return NoteScheme(id=db_note.id, text=db_note.text, list_id=db_note.list_id)

    async def get_all(self) -> list[NoteReadDTO]:
        """Retrieve all todo notes.

        Returns:
            A list of NoteReadDTO objects representing all todo notes.
            Returns empty list if no notes exist.

        """
        all_notes = await self.note_repo.list()
        if all_notes:
            return [
                NoteScheme(id=element.id, text=element.text, list_id=element.list_id)
                for element in all_notes
            ]
        return []

    async def create(self, text: str, list_id: UUID) -> NoteReadDTO:
        """Create a new todo note.

        Args:
            text: The text of the new note.
            list_id: The UUID of the list to which the note belongs.

        Returns:
            NoteReadDTO representing the newly created note.

        """
        db_note = await self.note_repo.add(
            data=Note(text=text, list_id=list_id), auto_commit=True
        )
        return NoteScheme(id=db_note.id, text=db_note.text, list_id=db_note.list_id)

    async def delete(self, note_id: UUID) -> NoteReadDTO:
        """Delete a todo note.

        Args:
            note_id: The UUID of the note to delete.

        Returns:
            NoteReadDTO representing the deleted note.

        """
        db_note = await self.note_repo.delete(item_id=note_id, auto_commit=True)
        return NoteScheme(id=db_note.id, text=db_note.text, list_id=db_note.list_id)


async def provide_list_service(db_session: AsyncSession) -> ListService:
    """Dependency provider for ListService.

    Args:
        db_session: AsyncSession for database operations.

    Returns:
        An instance of ListService configured with a ListRepository.

    """
    return ListService(ListRepository(session=db_session))


async def provide_note_service(db_session: AsyncSession) -> NoteService:
    """Dependency provider for NoteService.

    Args:
        db_session: AsyncSession for database operations.

    Returns:
        An instance of NoteService configured with a NoteRepository.

    """
    return NoteService(NoteRepository(session=db_session))
