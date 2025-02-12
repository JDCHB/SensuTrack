import mysql.connector
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.mascotas_model import Mascotas
from app.models.reporte_mascota_model import MascotasReport
from app.models.mascota_map_model import MascotasMap
from fastapi.encoders import jsonable_encoder


class CiegoController():

    def Mascotas_Map(self, mascotamap: MascotasMap):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT 
                    m.nombre AS nombre_mascota, 
                    c.latitud, 
                    c.longitud, 
                    cgps.numero_serie, 
                    cgps.nivel_bateria
                FROM 
                    mascota m
                JOIN 
                    coordenada c ON m.id = c.id_mascota
                LEFT JOIN 
                    collares_con_gps cgps ON cgps.id_mascota_vinculada = m.id
                WHERE 
                    m.id_propietario = %s
                ORDER BY 
                    m.nombre, c.create_f DESC
                LIMIT 25;
                """,
                (mascotamap.user_id,)
            )
            result = cursor.fetchall()
            payload = []

            # Recorremos cada fila de los resultados
            for data in result:
                content = {
                    'nombre_mascota': data[0],
                    'latitud': data[1],
                    'longitud': data[2],
                    'numero_serie': data[3],
                    'nivel_bateria': data[4]
                }
                payload.append(content)

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Mascotas no encontradas para el usuario"
                )

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, detail="Error en la base de datos")

        finally:
            conn.close()

        # MASCOTAS REPORTE

    def Mascotas_Report(self, mascotasreport: MascotasReport):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT
                mascota.id AS id_mascota,
                mascota.nombre,
                mascota.id_genero_mascota,
                mascota.id_tipo_mascota,
                mascota.id_propietario,
                mascota.fecha_hora,
                mascota.estado AS reporte_mascota
                FROM
                    mascota
                INNER JOIN
                    genero_mascota AS genero ON mascota.id_genero_mascota = genero.id
                INNER JOIN
                    tipo_mascota AS tipo ON mascota.id_tipo_mascota = tipo.id
                INNER JOIN
                    usuarios AS dueño ON mascota.id_propietario = dueño.id
                WHERE
                    mascota.fecha_hora BETWEEN %s AND %s
                LIMIT 0, 25;""", (mascotasreport.fecha1, mascotasreport.fecha2))
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'id_genero_mascota': int(data[2]),
                    'id_tipo_mascota': int(data[3]),
                    'id_propietario': int(data[4]),
                    'fecha_hora': data[5],
                    'estado': bool(data[6]),
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Mascota not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # CREAR MASCOTA
    def create_mascota(self, mascota: Mascotas):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mascota (nombre,id_genero_mascota,id_tipo_mascota,id_propietario,estado) VALUES (%s, %s, %s, %s, %s)",
                           (mascota.nombre, mascota.id_genero_mascota, mascota.id_tipo_mascota, mascota.id_propietario, mascota.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Mascota Registrada"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # BUSCAR MASCOTA
    def get_mascota(self, mascota_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM mascota WHERE id = %s", (mascota_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                "id": int(result[0]),
                "nombre": result[1],
                "id_genero_mascota": int(result[2]),
                "id_tipo_mascota": int(result[3]),
                "id_propietario": int(result[4]),
                "fecha_hora": result[5],
                'estado': bool(result[6]),
            }
            payload.append(content)

            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(
                    status_code=404, detail="Mascota not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # VER MASCOTAS
    def get_mascotas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascota")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'id_genero_mascota': int(data[2]),
                    'id_tipo_mascota': int(data[3]),
                    'id_propietario': int(data[4]),
                    'fecha_hora': data[5],
                    'estado': bool(data[6]),
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Mascota not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # ACTUALIZAR MASCOTA
    def update_mascota(self, mascota_id: int, mascota: Mascotas):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE mascota SET nombre = %s, genero = %s, estado = %s WHERE id = %s",
                           (mascota.nombre, mascota.genero, mascota.estado, mascota_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Mascota not found")
            return {"mensaje": "Datos de mascota actualizado exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    # ELIMINAR MASCOTA
    def delete_mascotas(self, mascota_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM mascota WHERE id = %s", (mascota_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Mascota no encontrada")
            return {"mensaje": "Mascota eliminada exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    # FIN MASCOTAS
