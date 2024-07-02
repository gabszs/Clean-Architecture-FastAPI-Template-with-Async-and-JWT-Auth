from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import Base
from app.models.models_enums import UserRoles


class User(Base):
    __tablename__ = "users"

    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    role: Mapped[UserRoles] = mapped_column(default=UserRoles.BASE_USER, server_default=UserRoles.BASE_USER)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="True")
