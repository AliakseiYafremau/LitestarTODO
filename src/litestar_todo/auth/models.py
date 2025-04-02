from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import Mapped, mapped_column


class User(base.UUIDAuditBase):
    """User model.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.

    """

    __tablename__ = "user"
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
