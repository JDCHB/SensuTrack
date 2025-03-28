from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.user_model import User, Login, Token, UserEstado
from app.controllers.user_controller import *

router = APIRouter()

nuevo_usuario = Usercontroller()


@router.post("/login_generate_token")
async def login_generate_token(user: Login):
    rpta = await nuevo_usuario.login_generate_token(user)
    return rpta


@router.post("/verify_token")
async def verify_token(token: Token):
    rpta = await nuevo_usuario.verify_token(token)
    return rpta


@router.post("/login")
async def login(user: Login):
    rpta = nuevo_usuario.login(user)
    return rpta


@router.post("/create_user")
async def create_user(user: User):
    rpta = nuevo_usuario.create_user(user)
    return rpta

# CARGUE MASIVO


@router.post("/create_usuario_masivo")
async def create_usuario_masivo(file: UploadFile = File(...)):
    rpta = nuevo_usuario.create_usuario_masivo(file)
    return rpta

# FIN CARGUE MASIVO


@router.get("/get_user/{user_id}", response_model=User)
async def get_user(user_id: int):
    rpta = nuevo_usuario.get_user(user_id)
    return rpta


@router.get("/get_users/")
async def get_users():
    rpta = nuevo_usuario.get_users()
    return rpta


@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: User):
    try:
        rpta = nuevo_usuario.update_user(user_id, user)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_user_admin/{user_id}")
async def update_user_admin(user_id: int, user: UPDATE_User):
    try:
        rpta = nuevo_usuario.update_user_admin(user_id, user)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_estado_user/{user_id}")
async def update_estado_user(user_id: int, user: UserEstado):
    try:
        rpta = nuevo_usuario.update_estado_user(user_id, user)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    try:
        rpta = nuevo_usuario.delete_user(user_id)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/Validar_Correo")
async def Validar_Correo(user: ValidarCorreo):
    rpta = nuevo_usuario.Validar_Correo(user)
    return rpta

@router.put("/update_contraseña")
async def update_contraseña(user: Login):
    try:
        rpta = nuevo_usuario.update_contraseña(user)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/Verificar_Google_User")
async def Verificar_Google_User(user: Google_user):
    rpta = nuevo_usuario.Verificar_Google_User(user)
    return rpta

@router.put("/Completar_Informacion/{user_id}")
async def Completar_Informacion(user_id: int, user: Completar_Informacion):
    try:
        rpta = nuevo_usuario.Completar_Informacion(user_id, user)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))