from fastapi import FastAPI,Request,HTTPException,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidation
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post.",
        "date_posted": "2024-06-01",
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post.",
        "date_posted": "2024-06-02",
    },
]

 
@app.get("/", include_in_schema=False,name="home")
@app.get("/posts",include_in_schema=False,name="posts")

def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html", 
        {"posts": posts,"title":"Home"}
                                         
    )



@app.get("/posts/{post_id}",include_in_schema=False,name="post_page")
def get_post(request:Request,post_id:int):
    for post in posts:
        if post.get("id")==post_id:
            title =post['title'] [:50]
            return templates.TemplateResponse(
                request,
                "post.html", 
                {"post": post, "title": title},

            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")



@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )