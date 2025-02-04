from typing import Optional, List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.models.base_model import Base
from app.models.models_enums import UserRoles


class Tenant(Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False)

    roles: Mapped[List["Role"]] = relationship(back_populates="tenant", cascade="all, delete-orphan", init=False)


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
    tenant: Mapped[Tenant] = relationship(back_populates="roles", init=False)

    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_tenant_name"),)
