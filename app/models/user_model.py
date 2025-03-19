from pydantic import BaseModel


class User(BaseModel):
    id: int = None
    email: str
    password: str
    nombre: str
    apellido: str
    documento: str
    telefono: str
    id_rol: int
    estado: bool


class UPDATE_User(BaseModel):
    id: int = None
    email: str
    nombre: str
    apellido: str
    documento: str
    telefono: str
    estado: bool


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str


class UserEstado(BaseModel):
    estado: bool

class ValidarCorreo(BaseModel):
    email: str


class Google_user(BaseModel):
    id: int= None
    id_usuario: int= None
    google_id: str
    foto: str
    access_token: str
    email: str
    nombre: str
    apellido: str
    estado: bool


class login_google(BaseModel):
    verif_user: Google_user
    user: User