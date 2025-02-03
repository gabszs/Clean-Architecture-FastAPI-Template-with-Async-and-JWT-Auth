from enum import Enum


class DatabaseType(str, Enum):
    MYSQL = "MYSQL"
    POSTGRES = "POSTGRES"
    REDIS = "REDIS"
    SQLSERVER = "SQLSERVER"
    MONGO = "MONGO"
    MARIA = "MARIA"


class UserRoles(str, Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    BASE_USER = "BASE_USER"
    GUEST = "GUEST"
