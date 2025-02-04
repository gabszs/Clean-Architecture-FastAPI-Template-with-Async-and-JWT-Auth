from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import Base
from app.models.models_enums import DatabaseType
from app.models.models_enums import UserRoles


class Tenant(Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True)
    role: Mapped[UserRoles] = mapped_column(default=UserRoles.BASE_USER, server_default=UserRoles.BASE_USER)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="True")


class Role(Base):
    __tablename__ = "roles"

    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]]

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_tenant_name"),)


class Database(Base):
    __tablename__ = "databases"

    # user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    db_type: Mapped[DatabaseType] = mapped_column(nullable=False)
    connection_string: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[Optional[str]]

    history: Mapped[List["History"]] = relationship(back_populates="database", cascade="all, delete-orphan", init=False)


class History(Base):
    __tablename__ = "history"

    name: Mapped[Optional[str]]
    schemas: Mapped[Optional[str]]
    database_id: Mapped[UUID] = mapped_column(ForeignKey("databases.id"))
    database: Mapped["Database"] = relationship(back_populates="history")
