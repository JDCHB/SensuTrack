from pydantic import BaseModel


class Dispositivo_GPS(BaseModel):
    id: int = None
    numero_serie: str
    nivel_bateria: int
    id_ciego_vinculado: int = None
    estado: bool

class GPSEstado(BaseModel):
    estado: bool

class ver_gps_con_Discapacitados(BaseModel):
    id: int = None
    numero_serie: str
    nombre: str

class ver_gps_con_Discapacitado(BaseModel):
    id: int = None
    numero_serie: str
    nombre: str
    estado: bool