from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from web.api import router  
import secrets
from fastapi.staticfiles import StaticFiles

app = FastAPI()
secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)
app.mount("/static", StaticFiles(directory="web/static"), name="static")
app.include_router(router)