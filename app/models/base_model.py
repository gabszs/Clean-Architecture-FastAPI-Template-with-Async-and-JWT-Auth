from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import text
from sqlalchemy import types
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.sql import func


class Base(MappedAsDataclass, DeclarativeBase):
    # __mapper_args__ = {"eager_defaults": True}
    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        init=False,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), init=False
    )
