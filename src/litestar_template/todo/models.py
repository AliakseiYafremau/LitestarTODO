from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from litestar.plugins.sqlalchemy import base


class List(base.UUIDAuditBase):
    __tablename__ = "list"
    title: Mapped[str]


class Note(base.UUIDAuditBase):
    __tablename__ = "note"
    text: Mapped[str]
    list_id: Mapped[UUID] = mapped_column(ForeignKey("list.id"))
