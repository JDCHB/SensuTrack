
from datetime import datetime, timedelta
import jwt
from fastapi import APIRouter, HTTPException, UploadFile, File, FastAPI
from app.controllers.token_controller import *
from app.models.user_model import Login,Token
from app.models.token_model import User_token

app = FastAPI()

router = APIRouter()

nuevo_usuario = TokenController()


@router.post("/generate_token")
async def generate_token(user: Login):
    rpta = nuevo_usuario.generate_token(user)
    return rpta


@router.post("/generate_token_google")
async def generate_token_google(user: User_token):
    rpta = nuevo_usuario.generate_token_google(user)
    return rpta


# @router.post("/verify_token")
# async def verify_token(token: Token):
#     rpta = nuevo_usuario.verify_token(token)
#     return rpta