from uuid import UUID

from litestar.plugins.sqlalchemy import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class List(base.UUIDAuditBase):
    """List model.

    Attributes:
        title (str): The title of the list.

    """

    __tablename__ = "list"
    title: Mapped[str]


class Note(base.UUIDAuditBase):
    """Note model.

    Attributes:
        text (str): The text of the note.
        list_id (UUID): The ID of the list to which the note belongs.

    """

    __tablename__ = "note"
    text: Mapped[str]
    list_id: Mapped[UUID] = mapped_column(ForeignKey("list.id"))
