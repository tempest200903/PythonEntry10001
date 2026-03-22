import os
from sqlalchemy import create_engine, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = os.environ["DATABASE_URL"]
SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace(
    "postgresql://", "postgresql+psycopg://", 1
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Counter(Base):
    __tablename__ = "counter_store"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


Base.metadata.create_all(engine)

with Session(engine) as session:
    counter = session.get(Counter, "main")
    if counter is None:
        counter = Counter(key="main", value=0)
        session.add(counter)
        session.flush()

    counter.value += 1
    session.commit()
    print("counter =", counter.value)
