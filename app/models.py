import sqlalchemy as sa
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
import uuid

class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(default=uuid.uuid4, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))
    email_address: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="users")


class Category(Base):

    __tablename__ = "category"

    category_id:Mapped[str] = mapped_column(default=uuid.uuid4, primary_key=True)
    category_name: Mapped[str] = mapped_column()

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="category")


class Task(Base):

    __tablename__ = "tasks"

    task_id: Mapped[str] = mapped_column(default=uuid.uuid4, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id", ondelete="cascade"))
    category_id: Mapped[str] = mapped_column(ForeignKey("category.category_id"))
    content: Mapped[str] = mapped_column()

    users: Mapped["User"] = relationship("User", back_populates="tasks")
    category: Mapped["Category"] = relationship("Category", back_populates="tasks")
    