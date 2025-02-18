from pydantic import BaseModel


class DiscapacitadoV(BaseModel):
    id: int = None
    nombre: str
    id_genero_discapacitado: int
    id_tipo_ceguera: int
    id_cuidador: int
    estado: bool

class CiegosReporte(BaseModel):
    fecha1: str
    fecha2: str