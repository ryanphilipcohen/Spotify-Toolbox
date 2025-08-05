from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import create_tables
from backend.app.routers.web import user, tag, track

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user")
app.include_router(tag.router, prefix="/tag")
app.include_router(track.router, prefix="/track")


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {"message": "Backend is working!"}
