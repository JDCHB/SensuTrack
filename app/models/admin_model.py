from pydantic import BaseModel
from typing import List, Optional


class NuevoCollar(BaseModel):
    numero_serie: str
    id_mascota_vinculada: int
    estado: bool
    # Nivel predeterminado si no se especifica
    nivel_bateria: int


class NuevoModulo(BaseModel):
    id: int = None
    nombre: str
    descripcion: str
    ubicacion: str
    estado: bool
    estilo: str


class Actualizar_Estado_Modulo(BaseModel):
    id: int = None
    estado: bool


class ModuloxRol(BaseModel):
    id: int = None
    id_modulo: List[int]
    id_rol: int
    estado: bool


class ModuloxRol_Can_See(BaseModel):
    id_rol: int = None
