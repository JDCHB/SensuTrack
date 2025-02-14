from pydantic import BaseModel


class Dispositivo_GPS(BaseModel):
    id: int = None
    numero_serie: str
    nivel_bateria: int
    fecha_hora_ultimo_reporte: str
    id_ciego_vinculado: int = None
    estado: bool

class GPSEstado(BaseModel):
    estado: bool