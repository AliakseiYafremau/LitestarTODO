from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from litestar_todo.todo.models import Note


class NoteRepository(SQLAlchemyAsyncRepository[Note]):
    """Repository for Note model."""

    model_type = Note

