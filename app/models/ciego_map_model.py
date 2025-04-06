from pydantic import BaseModel


class CiegosMap(BaseModel):
    user_id: int

class CiegoZonaS(BaseModel):
    nombre_zona: str
    latitud: str
    longitud: str
    id_discapacitado: int