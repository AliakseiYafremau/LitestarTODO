from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession

from litestar_todo.todo.models import Note


class NoteRepository(SQLAlchemyAsyncRepository[Note]):
    """Repository for Note model."""

    model_type = Note


async def provide_note_repo(db_session: AsyncSession) -> NoteRepository:
    """Dependency provider for NoteRepository.

    Args:
        db_session: AsyncSession for database operations.

    Returns:
        An instance of NoteRepository configured with a NoteRepository.

    """
    return NoteRepository(session=db_session)
