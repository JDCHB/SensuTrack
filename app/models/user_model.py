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

class CambioContraseña(BaseModel):
    email: str