from sqlalchemy import select, text
from sqlalchemy.orm import Session
from app.schemas import UserCreate, TaskCreate, CategoryCreate
from app.models import User, Task, Category

# user crud
def create_user(session: Session, user_in: UserCreate) -> User:
    user_in_dict = user_in.model_dump()
    new_user = User(**user_in_dict)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

def get_user_by_id(session: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.user_id == user_id)
    db_user = session.scalar(stmt)

    return db_user

def get_user_by_email(session: Session, email_address: str) -> User | None:
    stmt = select(User).where(User.email_address == email_address)
    db_user = session.scalar(stmt)

    return db_user

def delete_user(session: Session, user: User) -> None:
    session.delete(user)
    session.commit()
    
    return None
