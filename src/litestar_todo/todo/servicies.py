from __future__ import annotations

from typing import TYPE_CHECKING

from litestar_todo.todo.dto import (
    NoteReadScheme,
)
from litestar_todo.todo.models import Note
from litestar_todo.todo.repositories import NoteRepository

if TYPE_CHECKING:
    from uuid import UUID

    from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
    from sqlalchemy.ext.asyncio import AsyncSession


class NoteService:
    """Service for managing todo notes.

    Provides CRUD operations for todo notes using NoteRepository.
    """

    def __init__(self, note_repo: SQLAlchemyAsyncRepository) -> None:
        """Initialize the NoteService with a NoteRepository instance.

        Args:
            note_repo: The repository instance for database operations.

        """
        self.note_repo = note_repo

    async def get_by_id(self, note_id: UUID) -> NoteReadScheme | None:
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
        return NoteReadScheme(id=db_note.id, text=db_note.text)

    async def get_all(self) -> list[NoteReadScheme]:
        """Retrieve all todo notes.

        Returns:
            A list of NoteReadScheme objects representing all todo notes.
            Returns empty list if no notes exist.

        """
        all_notes = await self.note_repo.list()
        if all_notes:
            return [
                NoteReadScheme(
                    id=element.id,
                    text=element.text,
                )
                for element in all_notes
            ]
        return []

    async def create(self, text: str) -> NoteReadScheme | None:
        """Create a new todo note.

        Args:
            text: The text of the new note.

        Returns:
            NoteReadDTO representing the newly created note.

        """
        db_note = await self.note_repo.add(data=Note(text=text), auto_commit=True)
        return NoteReadScheme(id=db_note.id, text=db_note.text)

    async def delete(self, note_id: UUID) -> NoteReadScheme:
        """Delete a todo note.

        Args:
            note_id: The UUID of the note to delete.

        Returns:
            NoteReadDTO representing the deleted note.

        """
        db_note = await self.note_repo.delete(item_id=note_id, auto_commit=True)
        return NoteReadScheme(id=db_note.id, text=db_note.text)


async def provide_note_service(db_session: AsyncSession) -> NoteService:
    """Dependency provider for NoteService.

    Args:
        db_session: AsyncSession for database operations.

    Returns:
        An instance of NoteService configured with a NoteRepository.

    """
    return NoteService(NoteRepository(session=db_session))
