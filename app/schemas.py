from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    user_name: str = Field(max_length=30)
    email_address: str = Field(max_length=30)
    password: str = Field(max_length=30)


class CategoryCreate(BaseModel):
    category_name: str


class TaskBase(BaseModel):
    content: str = Field(max_length=255)
    category_id: str


class TaskCreate(TaskBase):
    user_id: str


class TaskUpdate(TaskBase):
    task_id: str

