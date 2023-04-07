from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.register import register_tortoise
from .db.config import TORTOISE_ORM

from .routers import users
from .routers import chats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(chats.router)

# register tortoise.
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get("/")
def home():
    return "Hello, World!"
