from enum import Enum


class UserRoles(str, Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    BASE_USER = "BASE_USER"
    GUEST = "GUEST"
