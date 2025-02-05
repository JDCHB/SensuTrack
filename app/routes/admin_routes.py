from fastapi import APIRouter, HTTPException
from app.models.admin_model import NuevoCollar, NuevoModulo, Actualizar_Estado_Modulo, ModuloxRol
from app.controllers.admin_controller import *

router = APIRouter()

nuevo_admin = AdminController()


@router.post("/create_collar")
async def create_collar(nuevocollar: NuevoCollar):
    rpta = nuevo_admin.create_collar(nuevocollar)
    return rpta


@router.post("/create_modulo")
async def create_modulo(nuevomodulo: NuevoModulo):
    rpta = nuevo_admin.create_modulo(nuevomodulo)
    return rpta


@router.post("/get_modulos_can_see")
async def get_modulos_can_see(moduloxrol_can_see: ModuloxRol_Can_See):
    rpta = nuevo_admin.get_modulos_can_see(moduloxrol_can_see)
    return rpta


@router.get("/get_modulo/{modulo_id}", response_model=NuevoModulo)
async def get_modulo(modulo_id: int):
    rpta = nuevo_admin.get_modulo(modulo_id)
    return rpta


@router.get("/get_modulos/")
async def get_modulos():
    rpta = nuevo_admin.get_modulos()
    return rpta


@router.put("/update_modulo/{modulo_id}")
async def update_modulo(modulo_id: int, nuevomodulo: NuevoModulo):
    try:
        rpta = nuevo_admin.update_modulo(modulo_id, nuevomodulo)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_estado_modulo/{modulo_id}")
async def update_estado_modulo(modulo_id: int, actualizar_estado_modulo: Actualizar_Estado_Modulo):
    try:
        rpta = nuevo_admin.update_estado_modulo(
            modulo_id, actualizar_estado_modulo)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_moduloXrol")
async def create_moduloXrol(moduloxrol: ModuloxRol):
    rpta = nuevo_admin.create_moduloXrol(moduloxrol)
    return rpta
