from fastapi import FastAPI, Query, Request, Depends, Form
from fastapi.responses import   JSONResponse, FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import database as db

class Login(BaseModel):
    email: str
    password: str

tamplates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

number: int = "hello" 

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
            return RedirectResponse(url=f"/task_list/{db_object.id}", status_code=303)
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

@app.get("/create_task/{id}")
def create_task(
    request: Request,
    id: int
    ):
    categories = db.get_categories()
    return tamplates.TemplateResponse(
        request=request,
        name = "create_task.html",
        # Add context header to frontend automaticaly change the header text
        context = {
            "id": id,
            "content": " ",
            "category": " ",
            "categories": categories,
            "header": "Create Task",
            "edit": False
            }
        )


@app.post("/create_task/{id}")
def get_create_task(
    id: int,
    task: str = Form(),
    category: int = Form()
    ):
    
    db_object = db.get_user(id)

    if db_object != None:
        db.create_task(id, content=task, category=category)
        return RedirectResponse(url=f"/task_list/{id}", status_code=303)
    else:
        return {"message": "something get wrong"}
    
@app.post("/delete_task")
def delete_task(task_id: int = Form()):

    db_object = db.get_task(task_id=task_id)

    if db_object != None:
        db.delete_tasks(task_id)
        return RedirectResponse(url=f"/task_list/{db_object.user_id}", status_code=303)
    else:
        return {"message": "task has not deleted"}
    
# Add endpoint edit to eding task
@app.get("/edit_task/{id}")
def edit_task(
    request: Request,
    id: int
    ):
    categories = db.get_categories()
    return tamplates.TemplateResponse(
        request=request,
        name = "create_task.html",
        # Add context header to frontend automaticaly change the header text
        context = {
            "id": id,
            "content": " ",
            "category": " ",
            "categories": categories,
            "header": "Create Task",
            "edit": False
            }
        )