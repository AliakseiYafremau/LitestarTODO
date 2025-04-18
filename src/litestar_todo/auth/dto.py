from uuid import UUID

import msgspec


class UserScheme(msgspec.Struct):
    """UserScheme class.

    Attributes:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        password (str): The password of the user.

    """

    id: UUID
    username: str
    password: str


class UserCreateScheme(msgspec.Struct):
    """UserCreateScheme class.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.

    """

    username: str
    password: str


class UserReadScheme(msgspec.Struct):
    """UserReadScheme class.

    Attributes:
        id (str): The unique identifier of the user.
        username (str): The username of the user.

    """

    id: UUID
    username: str


class TokenScheme(msgspec.Struct):
    """TokenScheme class.

    Attributes:
        access_token (str): The access token for the user.
        token_type (str): The type of the token.

    """

    access_token: str
    token_type: str
