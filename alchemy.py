from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

from sqlalchemy import MetaData
# metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String
# user_table = Table(
#     "user_account",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(30)),
#     Column("fullname", String),
# )

# # print(repr(user_table.c.id))

from sqlalchemy import ForeignKey
# address_table = Table(
#     "address",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("user_id", ForeignKey("user_account.id"), nullable=False),
#     Column("email_address", String, nullable=False),
# )

# metadata_obj.create_all(engine)

from sqlalchemy.orm import DeclarativeBase, Session
class Base(DeclarativeBase):
    pass

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

print('Creating tables from Base metadata')
Base.metadata.create_all(engine)

squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

session = Session(engine)
session.add(squidward)
print(f"Squidward ID: {squidward.id}")
session.add(krabs)
session.flush()
print(f"Krabs ID: {krabs.id}")
some_squidward = session.get(User, 1)
print(some_squidward)
print(some_squidward is squidward)