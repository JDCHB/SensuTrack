from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.atributo_routes import router as atributo_router
from app.routes.atributoxusuario_routes import router as atributoxuser_router
from app.routes.ciego_routes import router as ciego_router
from app.routes.roles_routes import router as roles_router
from app.routes.tipo_mascota_routes import router as tipo_mascota_router
from app.routes.genero_mascota_routes import router as genero_mascota_router
from app.routes.gps_routes import router as gps_router
from app.routes.admin_routes import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(atributo_router)
app.include_router(atributoxuser_router)
app.include_router(ciego_router)
app.include_router(roles_router)
app.include_router(tipo_mascota_router)
app.include_router(genero_mascota_router)
app.include_router(gps_router)
app.include_router(admin_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
