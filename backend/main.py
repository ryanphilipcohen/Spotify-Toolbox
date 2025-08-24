from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import create_tables
from backend.app.routers.web import user, tag, track


"""
This is the file that's run to start the backend server.
FastAPI is a framework used to create an API.

CORS middleware is used to allow requests from specific locations.
In this case, it's allowing requests from our frontend running on localhost:5173.
"""
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Routers are used to organize the API endpoints.
In theory, you can include all API endpoints (or routes) in one file. It'd be long.
"""
app.include_router(user.router, prefix="/user")
app.include_router(tag.router, prefix="/tag")
app.include_router(track.router, prefix="/track")


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {"message": "Backend is working!"}
