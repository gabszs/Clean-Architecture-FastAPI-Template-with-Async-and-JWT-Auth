from enum import Enum


class DatabaseType(str, Enum):
    MYSQL: "MYSQL"
    POSTGRES: "POSTGRES"
    REDIS: "REDIS"
    SQLSERVER: "SQLSERVER"
    MONGO: "MONGO"
    MARIA: "MARIA"
