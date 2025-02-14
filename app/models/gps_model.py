from pydantic import BaseModel


class Dispositivo_GPS(BaseModel):
    id: int = None
    numero_serie: str
    latitud: str
    longitud: str
    nivel_bateria: int
    id_mascota_vinculada: int = None
    estado: bool

class GPSEstado(BaseModel):
    estado: bool