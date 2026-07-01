from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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



@app.get("/api/posts")
def get_posts():
    return posts
