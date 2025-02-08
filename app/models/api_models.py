from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Tenant(Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[List["UserTenant"]] = relationship(back_populates="tenant", init=False)
    roles: Mapped[List["Role"]] = relationship(back_populates="tenant", cascade="all, save-update", init=False)


class UserTenant(Base):
    __tablename__ = "user_tenants"
    # __table_args__ = (UniqueConstraint("user_id", "tenant_id", name="uq_user_role"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id"))
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="tenants", init=False)
    tenant: Mapped[Tenant] = relationship(back_populates="users", init=False)


class User(Base):
    __tablename__ = "users"
    eagers = ["roles", "tenants"]

    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True)

    roles: Mapped[List["UserRole"]] = relationship(back_populates="user", init=False)
    tenants: Mapped[List["UserTenant"]] = relationship(back_populates="user", init=False)

    is_active: Mapped[bool] = mapped_column(default=True, server_default="True")


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_tenant_name"),)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]]
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id", ondelete="SET NULL"))
    tenant: Mapped[Tenant] = relationship(back_populates="roles", init=False)

    users: Mapped[List["UserRole"]] = relationship(back_populates="role", init=False)


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"))
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="roles", init=False)
    role: Mapped["Role"] = relationship(back_populates="users", init=False)
