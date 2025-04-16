from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from typing import Sequence, Tuple, Optional

from src.config import Config
from .models.base import Base
from .models.coterie import Coterie
from .models.teacher import Teacher
from .models.type import Type
from .models.adress import Address


class Helper:
    def __init__(self):
        self.engine = create_engine(Config.DB_URL)
        Base.metadata.create_all(self.engine)

    def get_coteries(self) -> Sequence[Coterie]:
        with Session(self.engine) as session:
            return session.scalars(select(Coterie)).all()

    def get_coterie(self, id_: int) -> Optional[Coterie]:
        with Session(self.engine) as session:
            return session.scalars(select(Coterie).where(id_ == Coterie.id)).one_or_none()

    def get_types(self) -> Sequence[Type]:
        with Session(self.engine) as session:
            return session.scalars(select(Type)).all()

    def get_teachers(self) -> Sequence[Teacher]:
        with Session(self.engine) as session:
            return session.scalars(select(Teacher)).all()

    def get_teacher(self, id_: int) -> Optional[Teacher]:
        with Session(self.engine) as session:
            return session.scalars(select(Teacher).where(id_ == Teacher.id)).one_or_none()

    def get_addresses(self) -> Sequence[Address]:
        with Session(self.engine) as session:
            return session.scalars(select(Address)).all()

    def get_address(self, id_: int) -> Optional[Address]:
        with Session(self.engine) as session:
            return session.scalars(select(Address).where(id_ == Address.id)).one_or_none()

    def add_teacher(self, name: str = None, photo_url: str = None, link: str = None) -> Tuple[bool, str]:
        if not all([name, photo_url, link]):
            return False, "no-data"
        with Session(self.engine) as session:
            if session.scalars(select(Teacher).where(Teacher.name == name)).one_or_none() is not None:
                return False, "already-exists"
            teacher = Teacher(name=name, photo_url=photo_url, link=link)
            session.add(teacher)
            session.commit()
            return True, teacher.id

    def edit_teacher(self, id_: int = None, new_name: str = None, new_photo_url: str = None, new_link: str = None) -> \
            Tuple[bool, str]:
        if id_ is None:
            return False, "no-id"
        with Session(self.engine) as session:
            teacher = session.scalars(select(Teacher).where(Teacher.id == id_)).one_or_none()
            if teacher is None:
                return False, "not-found"
            if new_name is not None:
                teacher.name = new_name
            if new_photo_url is not None:
                teacher.photo_url = new_photo_url
            if new_link is not None:
                teacher.link = new_link
            session.commit()
            return True, "ok"

    def delete_teacher(self, id_: int = None):
        return self._delete(Teacher, id_)

    def add_address(self, address: str = None) -> Tuple[bool, str]:
        if address is None:
            return False, "no-data"
        with Session(self.engine) as session:
            if session.scalars(select(Address).where(Address.address == address)).one_or_none() is not None:
                return False, "already-exists"
            address = Address(address=address)
            session.add(address)
            session.commit()
            return True, address.id

    def edit_address(self, id_: int = None, new_address: str = None) -> Tuple[bool, str]:
        if id_ is None:
            return False, "no-id"
        with Session(self.engine) as session:
            address = session.scalars(select(Address).where(Address.id == id_)).one_or_none()
            if address is None:
                return False, "not-found"
            if new_address is not None:
                address.address = new_address
            session.commit()
            return True, "ok"

    def delete_address(self, id_: int = None):
        return self._delete(Address, id_)

    def add_coterie(self, name: str = None, type_id: int = None, teacher_id: int = None, address_id: int = None,
                    beg_age: int = None, end_age: int = None, day: str = None, price: bool = None, info: str = None,
                    url: str = None):
        if not all(map(lambda x: x is not None,
                       [name, type_id, teacher_id, address_id, beg_age, end_age, day, price, info, url])):
            return False, "no-data"
        type_id = int(type_id)
        with Session(self.engine) as session:
            if 1 >= type_id >= 5:
                return False, "wrong-type_id"
            teacher = session.scalars(select(Teacher).where(Teacher.id == teacher_id)).one_or_none()
            if teacher is None:
                return False, "wrong-teacher_id"
            address = session.scalars(select(Address).where(Address.id == address_id)).one_or_none()
            if address is None:
                return False, "wrong-address_id"
            coterie = Coterie(name=name, type_id=type_id, teacher_id=teacher_id, address_id=address_id,
                              beg_age=beg_age, end_age=end_age, day=day, price=float(price), info=info, url=url)
            session.add(coterie)
            session.commit()
            return True, coterie.id

    def edit_coterie(self, id_: int = None, new_name: str = None, new_type_id: int = None, new_teacher_id: int = None,
                     new_address_id: int = None, new_beg_age: int = None, new_end_age: int = None, new_day: str = None,
                     new_price: bool = None, new_info: str = None, new_url: str = None):
        if id_ is None:
            return False, "no-id"
        with Session(self.engine) as session:
            coterie = session.scalars(select(Coterie).where(Coterie.id == id_)).one_or_none()
            if coterie is None:
                return False, "not-found"
            if new_name is not None and new_name:
                coterie.name = new_name
            if new_type_id is not None:
                if 1 >= int(new_type_id) >= 5:
                    return False, "wrong-type_id"
                coterie.type_id = new_type_id
            if new_teacher_id is not None:
                teacher = session.scalars(select(Teacher).where(Teacher.id == new_teacher_id)).one_or_none()
                if teacher is None:
                    return False, "wrong-teacher_id"
                coterie.teacher_id = new_teacher_id
            if new_address_id is not None:
                address = session.scalars(select(Address).where(Address.id == new_address_id)).one_or_none()
                if address is None:
                    return False, "wrong-address_id"
                coterie.address_id = new_address_id
            if new_beg_age is not None:
                coterie.beg_age = new_beg_age
            if new_end_age is not None:
                coterie.end_age = new_end_age
            if new_day is not None:
                coterie.day = new_day
            if new_price is not None:
                coterie.price = float(new_price)
            if new_info is not None and new_info:
                coterie.info = new_info
            if new_url is not None and new_url:
                coterie.url = new_url
            session.commit()
            return True, "ok"

    def delete_coterie(self, id_: int = None):
        return self._delete(Coterie, id_)

    def _delete(self, cls, id_):
        if id_ is None:
            return False, "no-id"
        with Session(self.engine) as session:
            c = session.scalars(select(cls).where(cls.id == id_)).one_or_none()
            if c is None:
                return False, "not-found"
            session.delete(c)
            session.commit()
            return True, "ok"
