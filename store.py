import os
from sqlalchemy import create_engine, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = os.environ["DATABASE_URL"]
SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace(
    "postgresql://", "postgresql+psycopg://", 1
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def save_dataframe(df):
    df.to_sql("cost", engine, if_exists="replace", index=False)
