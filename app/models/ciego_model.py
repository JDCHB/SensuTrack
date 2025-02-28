from pydantic import BaseModel

class DiscapacitadoV(BaseModel):
    id: int = None
    nombre: str
    id_genero_discapacitado: int
    id_tipo_ceguera: int
    id_cuidador: int
    estado: bool

class Ciegos_Report(BaseModel):
    id: int = None
    nombre: str
    genero: str  # Ahora es un string, ya que estamos mostrando el nombre del género, no el ID.
    tipo_ceguera: str  # Similar para tipo de ceguera.
    nombre_cuidador: str  # Nombre del cuidador, no su ID.
    fecha: str  # Mantener la fecha como string.
    estado: bool

class CiegosReporte(BaseModel):
    fecha1: str
    fecha2: str

class DiscapacitadoEstado(BaseModel):
    estado: bool