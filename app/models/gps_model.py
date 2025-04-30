from pydantic import BaseModel


class Dispositivo_GPS(BaseModel):
    id: int = None
    numero_serie: str
    nivel_bateria: int
    id_ciego_vinculado: int = None
    estado: bool

class GPSEstado(BaseModel):
    id: int = None
    estado: bool

class ver_gps_con_Discapacitado(BaseModel):
    id: int = None
    numero_serie: str
    nombre: str
    estado: bool

class get_serial_bateria_GPS(BaseModel):
    documento: str

class CoordenadaDiscapacitado(BaseModel):
    latitud: float
    longitud: float