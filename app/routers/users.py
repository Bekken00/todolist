from fastapi import APIRouter, HTTPException

from schemas import UserCreate
from dependencies import SessionDep
import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create_user")
def create_user(session: SessionDep, user_in: UserCreate):
    user = crud.create_user(session=session, user_in=user_in)

    return user


@router.delete("/delete_user/{user_id}")
def delete_user(session: SessionDep, user_id: str):
    db_user = crud.get_user_by_id(session=session, user_id=user_id)
    if db_user == None:
        raise HTTPException(
            status_code=404, detail="User did not found"
        )
    else:
        crud.delete_user(session=session, user=db_user)
