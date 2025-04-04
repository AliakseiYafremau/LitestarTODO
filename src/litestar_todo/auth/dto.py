import msgspec


class UserScheme(msgspec.Struct):
    """UserScheme class.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.

    """

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


class UserReadDTO(msgspec.Struct):
    """UserReadDTO class.

    Attributes:
        username (str): The username of the user.

    """

    username: str
