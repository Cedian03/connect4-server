import os

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from connect4_server.database import lifespan

from connect4_server.auth.router import router as auth_router
from connect4_server.game.router import router as game_router
from connect4_server.user.router import router as user_router


FRONTEND_ORIGINS = os.environ.get(
    "FRONTEND_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app = FastAPI(lifespan=lifespan, root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(game_router)


@app.get(
    "/",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
)
def root():
    return f"{app.root_path}/docs"
