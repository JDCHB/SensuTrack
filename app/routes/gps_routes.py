from fastapi import APIRouter, HTTPException
from app.models.gps_model import *
from app.controllers.gps_controller import *
from app.controllers.ciego_controller import *
router = APIRouter()

nueva_unidad_gps = GPScontroller()

@router.post("/create_gps")
async def create_gps(dispositivo_gps: Dispositivo_GPS):
    rpta = nueva_unidad_gps.create_gps(dispositivo_gps)
    return rpta


@router.get("/get_gps/{gps_id}", response_model=Dispositivo_GPS)
async def get_gps(gps_id: int):
    try:
        rpta = nueva_unidad_gps.get_gps(gps_id)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_Unidadesgps/")
async def get_Unidadesgps():
    rpta = nueva_unidad_gps.get_Unidadesgps()
    return rpta


@router.put("/update_gps/{gps_id}")
async def update_gps(gps_id: int, dispositivo_gps: Dispositivo_GPS):
    try:
        rpta = nueva_unidad_gps.update_gps(
            gps_id, dispositivo_gps)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_estado_GPS/{gps_id}")
async def update_estado_GPS(gps_id: int, gpsestado: GPSEstado):
    try:
        rpta = nueva_unidad_gps.update_estado_GPS(gps_id, gpsestado)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_gps/{gps_id}")
async def delete_gps(gps_id: int):
    try:
        rpta = nueva_unidad_gps.delete_gps(gps_id)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_GPS_Discapacitados/")
async def get_GPS_Discapacitados():
    rpta = nueva_unidad_gps.get_GPS_Discapacitados()
    return rpta

@router.get("/get_GPS_Discapacitado/{gps_id}", response_model=ver_gps_con_Discapacitado)
async def get_GPS_Discapacitado(gps_id: int):
    try:
        rpta = nueva_unidad_gps.get_GPS_Discapacitado(gps_id)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get_Serial_GPS")
async def get_Serial_GPS(serial: get_serial_bateria_GPS):
    rpta = nueva_unidad_gps.get_Serial_GPS(serial)
    return rpta

@router.put("/update_coordenadas_discapacitado/{discapacitado_id}")
async def update_coordenadas_discapacitado(discapacitado_id: int, coord: CoordenadaDiscapacitado):
    try:
        rpta = nueva_unidad_gps.update_coordenadas_discapacitado(discapacitado_id, coord)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))