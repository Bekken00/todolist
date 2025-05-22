from fastapi import FastAPI, Query, Request, Depends, Form
from fastapi.responses import   JSONResponse, FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import database as db

tamplates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root(request: Request):
    return tamplates.TemplateResponse(
        request=request,
        name="index.html", 
        context={"text": "Welcome to To-Do list "}
    )

@app.get("/login")
def login(request: Request):
    
    return tamplates.TemplateResponse(
        request=request,
        name="login.html", 
        context={
            "message_email": " ",
            "message_password": " "
        }
    )

@app.post("/login/")
def get_login(
    request: Request, 
    email: str = Form(), 
    password: str = Form()
    ):
    
    db_object = db.get_user_by_email(email)

    message_email = " "
    message_password = " "

    if db_object != None:
        if db_object.password == password:
            return RedirectResponse(url=f"/task_list/{db_object.user_id}", status_code=303)
        else:
            message_password = "wrong password"
    else:
        message_email = "email did not found"

    return tamplates.TemplateResponse(
        request=request,
        name="login.html", 
        context={
            "email": email,
            "password": password,
            "message_email": message_email,
            "message_password": message_password
        }
    )

@app.get("/register")
def register(request: Request):

    return tamplates.TemplateResponse(
        request = request,
        name = "register.html"
    )

@app.post("/register/")
def get_register(
    request: Request, 
    name: str = Form(), 
    email: str = Form(), 
    password: str = Form(), 
    repeated_password: str = Form()
    ):

    db_object = db.get_user_by_email(email)
    message_email = " "
    message_password = " "
    
    if db.check_email(email):
        if db_object == None:
            if db.check_password(password):
                if password == repeated_password:
                    message_email = "You registered successfully"
                    db.create_user(name, email, password)
                else:
                    message_password = "Your repeated password does not same"
            else:
                message_password = "Password have to include 8 letter, 1 upper, 1 lower, 1 digit"
        else:
            message_email = "Email already exist"
    else:
        message_email = "Wrong email"

    return tamplates.TemplateResponse(
        request = request,
        name = "register.html",
        context = {
            "name": name,
            "email": email,
            "password": password,
            "repeated_password": repeated_password,
            "message_email": message_email,
            "message_password": message_password
        }
    )

@app.get("/task_list/{id}")
def get_tasks(
    request: Request,
    id: int
    ):

    items = db.get_tasks(id)

    return tamplates.TemplateResponse(
        request = request,
        name = "task_list.html",
        context = {
            "items": items,
            "id": id
            }
    )

@app.get("/create_task/{user_id}")
def create_task(
    request: Request,
    user_id: int
    ):
    categories = db.get_categories()
    return tamplates.TemplateResponse(
        request=request,
        name = "create_task.html",
        context = {
            "user_id": user_id,
            "content": " ",
            "category": " ",
            "categories": categories,
            "header": "Create Task",
            "edit": False
            }
        )


@app.post("/create_task/{user_id}")
def get_create_task(
    user_id: int,
    task: str = Form(),
    category: int = Form()
    ):
    
    db_object = db.get_user(user_id)

    if db_object != None:
        db.create_task(user_id, content=task, category_id=category)
        return RedirectResponse(url=f"/task_list/{user_id}", status_code=303)
    else:
        return {"message": "user not found"}
    
@app.post("/delete_task")
def delete_task(task_id: int = Form()):

    db_object = db.get_task(task_id=task_id)

    if db_object != None:
        db.delete_tasks(task_id)
        return RedirectResponse(url=f"/task_list/{db_object.user_id}", status_code=303)
    else:
        return {"message": "task has not deleted"}
    
@app.get("/edit_task/{task_id}")
def edit_task(
    request: Request,
    task_id: int
    ):
    categories = db.get_categories()
    task = db.get_task(task_id=task_id)
    return tamplates.TemplateResponse(
        request=request,
        name = "create_task.html",
        context = {
            "task_id": task_id,
            "content": task.content,
            "category": task.category_id,
            "categories": categories,
            "header": "Edit task",
            "edit": True
            }
        )

@app.post("/edit_task/{task_id}")
def get_edit_task(
    task_id: int,
    task: str = Form(),
    category: int = Form()
    ):
    db_object = db.get_task(task_id = task_id)
    if db_object != None:
        db.edit_task(task_id = task_id, content = task, category_id = category)
        return RedirectResponse(url=f"/task_list/{db.get_user_by_task(task_id)}", status_code=303)
    else:
        return {"message": "task has not found"}
