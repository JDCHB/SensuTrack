from pydantic import BaseModel


class Dispositivo_GPS(BaseModel):
    id: int = None
    numero_serie: str
    nivel_bateria: int
    id_ciego_vinculado: int = None
    estado: bool

class GPSEstado(BaseModel):
    estado: bool