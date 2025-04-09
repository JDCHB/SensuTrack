from pydantic import BaseModel


class CiegosMap(BaseModel):
    user_id: int

class CiegoZonaS(BaseModel):
    id: int = None
    nombre_zona: str
    latitud: str
    longitud: str
    radio: float
    id_discapacitado: int
    estado: bool

class CiegoZonaSUPDATE(BaseModel):
    id: int = None
    nombre_zona: str
    latitud: str
    longitud: str
    radio: float

# class CiegoZonaSESTADO(BaseModel):
#     estado: bool