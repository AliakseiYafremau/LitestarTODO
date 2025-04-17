from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import Mapped


class Note(base.UUIDAuditBase):
    """Note model.

    Attributes:
        text (str): The text of the note.

    """

    __tablename__ = "note"
    text: Mapped[str]
