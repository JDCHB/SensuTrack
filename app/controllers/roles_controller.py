import mysql.connector
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.roles_model import Roles, Actualizar_Estado_Rol
from fastapi.encoders import jsonable_encoder


class Rolescontroller():

    # CREAR ROL
    def create_rol(self, roles: Roles):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO roles (nombre, estado) VALUES (%s, %s)",
                           (roles.nombre, roles.estado,))
            conn.commit()
            conn.close()
            return {"resultado": "Rol creado"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # BUSCAR ROL
    def get_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM roles WHERE id = %s", (rol_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                'id': int(result[0]),
                'nombre': result[1],
                'estado': bool(result[2]),
            }
            payload.append(content)

            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(
                    status_code=404, detail="Rol not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # VER ROLES
    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roles")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'estado': bool(data[2]),
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Roles not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # ACTUALIZAR ROL
    def update_rol(self, rol_id: int, roles: Roles):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE roles SET nombre = %s, estado = %s WHERE id = %s",
                (roles.nombre, roles.estado, rol_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Rol no encontrado")

            return {"mensaje": "Rol actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()

    # ELIMINAR ROL
    def delete_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM roles WHERE id = %s", (rol_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Rol no encontrado")
            return {"mensaje": "Rol eliminado exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    # ACTUALIZAR ESTADO DEL MODULO
    def update_estado_rol(self, rol_id: int, actualizar_estado_rol: Actualizar_Estado_Rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE roles SET estado = %s WHERE id = %s",
                (actualizar_estado_rol.estado, rol_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Rol no encontrado")

            return {"mensaje": "Estado de Rol actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()
