from fastapi import APIRouter

from dependencies import SessionDep
import crud

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/get_tasts/{user_id}")
def get_tasks(session: SessionDep, user_id: str):
    pass
