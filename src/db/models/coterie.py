from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base
from .type import Type
from .teacher import Teacher
from .adress import Address


class Coterie(Base):
    __tablename__ = "coterie"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped["Type"] = relationship(lazy="joined")
    type_id: Mapped[int] = mapped_column(ForeignKey("type.id"))
    teacher: Mapped["Teacher"] = relationship(lazy="joined")
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    address: Mapped["Address"] = relationship(lazy="joined")
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))
    beg_age: Mapped[int]
    end_age: Mapped[int]
    day: Mapped[str]
    price: Mapped[float]
    info: Mapped[str]
    url: Mapped[str]
