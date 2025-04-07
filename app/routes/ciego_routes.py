from fastapi import APIRouter, HTTPException
from app.models.ciego_model import *
from app.models.ciego_map_model import *
from app.controllers.ciego_controller import *

router = APIRouter()

nuevo_discapacitado = CiegoController()


@router.post("/Ciegos_Map")
async def Ciegos_Map(mascotamap: CiegosMap):
    rpta = nuevo_discapacitado.Ciegos_Map(mascotamap)
    return rpta

@router.post("/create_Zona_Segura")
async def create_Zona_Segura(ciegozonas: CiegoZonaS):
    rpta = nuevo_discapacitado.create_Zona_Segura(ciegozonas)
    return rpta

@router.get("/get_Zona_Segura/{discapacitado_id}", response_model=CiegoZonaS)
async def get_Zona_Segura(discapacitado_id: int):
    try:
        rpta = nuevo_discapacitado.get_Zona_Segura(discapacitado_id)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/Ciegos_Report")
async def Ciegos_Report(ciegosreporte: CiegosReporte):
    rpta = nuevo_discapacitado.Ciegos_Report(ciegosreporte)
    return rpta

@router.post("/create_discapacitadoV")
async def create_discapacitadoV(discapacitadov: DiscapacitadoV):
    rpta = nuevo_discapacitado.create_discapacitadoV(discapacitadov)
    return rpta

@router.get("/get_discapacitadoV/{discapacitado_id}", response_model=DiscapacitadoV)
async def get_discapacitadoV(discapacitado_id: int):
    try:
        rpta = nuevo_discapacitado.get_discapacitadoV(discapacitado_id)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_discapacitadosV/")
async def get_discapacitadosV():
    rpta = nuevo_discapacitado.get_discapacitadosV()
    return rpta

@router.get("/get_discapacitadosVCOMPLETOS")
async def get_discapacitadosVCOMPLETOS():
    rpta = nuevo_discapacitado.get_discapacitadosVCOMPLETOS()
    return rpta

@router.get("/get_discapacitadosV_SIN_GPS/")
async def get_discapacitadosV_SIN_GPS():
    rpta = nuevo_discapacitado.get_discapacitadosV_SIN_GPS()
    return rpta

@router.put("/update_discapacitadoV/{discapacitado_id}")
async def update_discapacitadoV(discapacitado_id: int, discapacitadov: DiscapacitadoV):
    try:
        rpta = nuevo_discapacitado.update_discapacitadoV(discapacitado_id, discapacitadov)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_discapacitadoV/{discapacitado_id}")
async def delete_discapacitadoV(discapacitado_id: int):
    try:
        rpta = nuevo_discapacitado.delete_discapacitadoV(discapacitado_id)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_estado_discapacitado/{discapacitado_id}")
async def update_estado_discapacitado(discapacitado_id: int, discapacitadoestado: DiscapacitadoEstado):
    try:
        rpta = nuevo_discapacitado.update_estado_discapacitado(discapacitado_id, discapacitadoestado)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
