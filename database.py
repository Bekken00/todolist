from typing import List
from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from fastapi import Depends

from sqlalchemy.exc import NoResultFound

import random


engine = create_engine("sqlite:///database.db", echo=True, connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    pass



class User(Base):

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column()
    email_adress: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="users", cascade="all, delete")



class Category(Base):

    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column()

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="category")



class Task(Base):

    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    content: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"))
    status: Mapped[bool] = mapped_column(default=False)

    users: Mapped["User"] = relationship("User", back_populates="tasks")
    category: Mapped["Category"] = relationship("Category", back_populates="tasks")


Base.metadata.create_all(bind=engine)


session = Session(engine, autoflush=False)


def create_user(user_name: str, email: str, password: str):

    new_user = User(
        user_name = user_name,
        email_adress = email,
        password = password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()


def create_category(category_name: str):

    new_category = Category(
        category_name = category_name
    )

    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    session.close()


def create_task(user_id: int, content: str, category_id: int):
    
    new_task = Task(
        user_id = user_id,
        content = content,
        category_id = category_id
    )


    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    session.close()


def get_user(user_id: int):
    stmt = select(User).where(User.user_id == user_id)
    try:
        session.scalars(stmt).one()
    except NoResultFound:
        db_object = None
    else:
        db_object = session.scalars(stmt).one()
    

    return db_object

def get_user_by_email(email: str):
    stmt = select(User).where(User.email_adress == email)
    try:
        session.scalars(stmt).one()
    except NoResultFound:
        db_object = None
    else:
        db_object = session.scalars(stmt).one()

    return db_object


def get_task(task_id: int):
    stmt = select(Task).where(Task.task_id == task_id)
    try:
        session.scalars(stmt).one()
    except NoResultFound:
        db_object = None
    else:
        db_object = session.scalars(stmt).one()

    return db_object

def get_user_by_task(task_id: int):
    task = get_task(task_id)
    user_id = task.user_id

    return user_id

def get_tasks(user_id: int):
    stmt = select(Task).where(Task.user_id == user_id)
    try:
        session.scalars(stmt).all()
    except NoResultFound:
        db_object = None
    else:
        db_object = session.scalars(stmt).all()

    return db_object


def get_category(category_id: int): 
    stmt = select(Category).where(Category.category_id == category_id)
    try:
        session.scalars(stmt).one()
    except NoResultFound:
        db_object = None
    else:
        db_object = session.scalars(stmt).one()

    return db_object


def get_categories():
    stmt = select(Category)
    try:
        session.scalars(stmt).all()
    except NoResultFound:
        db_object = None
    else:
        db_object = session.scalars(stmt).all()

    return db_object


def get_email(email: str):
    stmt = select(User).where(User.email_adress == email)
    try:
        session.scalars(stmt).one()
    except NoResultFound:
        db_object = None
    else:
        db_object = session.scalars(stmt).one()

    return db_object


def get_password(user_id: int, password: str) -> User | None:
    db_object = get_user(user_id)
    if db_object != None:
        if db_object.password == password:
            return db_object
        
    return None

def delete_user(user_id: int):
    db_object = get_user(user_id)
        
    if db_object != None:
        session.delete(db_object)
        session.commit()
        session.close()

    return db_object


def delete_tasks(task_id: int): 
    db_object = get_task(task_id)    
    
    if db_object != None:
        session.delete(db_object)
        session.commit()
        session.close()

    return db_object


def edit_task(task_id: int, content: str, category_id: int):
    db_object = get_task(task_id)

    if db_object != None:
        db_object.content = content
        db_object.category_id = category_id
        session.commit()
        session.close()

    return db_object


def make_category():
    categories = ["work", "study", "hobby", "self", "others"]

    for elem in categories:
        create_category(elem)


def check_email(email: str) -> bool:
    email = email.strip()

    if email.islower():
        if email.endswith(("@gmail.com", "@mail.ru")):
            if len(email) > 10:
                if " " not in email:
                    return True
    
    return False
    

def check_password(password: str) -> bool:
    password = password.strip()

    if len(password) >= 8:
        if password.islower() != True:
            if password.isupper() != True:
                if password.isalpha() != True:
                    if password.isdigit() != True:
                        if " " not in password:
                            return True
                
    return False


def get_tasks_with_category(user_id: int):
    get_tasks(user_id)

def make_tasks():
    tasks = ["do the home work", "make a project", "find the keys", "go to work", "write the letter"]

    for task in tasks:
        create_task(1, task, random.randint(1, 5))

def make():
    stmt = select(Task.category).where(Task.task_id == 1)

    return session.scalars(stmt).all()
