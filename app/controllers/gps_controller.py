import mysql.connector
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.gps_model import *
from fastapi.encoders import jsonable_encoder


class GPScontroller():

    # CREAR UNIDADGPS
    def create_gps(self, dispositivo_gps: Dispositivo_GPS):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO unidad_gps (numero_serie, nivel_bateria, fecha_hora_ultimo_reporte, id_ciego_vinculado, estado) VALUES (%s, %s, %s, %s, %s)",
                           (dispositivo_gps.numero_serie, dispositivo_gps.nivel_bateria, dispositivo_gps.fecha_hora_ultimo_reporte, dispositivo_gps.id_ciego_vinculado, dispositivo_gps.estado,))
            conn.commit()
            conn.close()
            return {"resultado": "UnidadGPS Registrado exitosamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Error durante la inserción: {err}")
        finally:
            if conn:
                conn.close()

    # BUSCAR COLLARGPS
    def get_gps(self, gps_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM unidad_gps WHERE id = %s", (gps_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                "id": int(result[0]),
                "numero_serie": result[1],
                "nivel_bateria": result[2],
                "fecha_hora_ultimo_reporte": result[3],
                "id_ciego_vinculado": int(result[4]),
                'estado': bool(result[5]),
            }
            payload.append(content)

            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(
                    status_code=404, detail="UnidadGPS not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # VER COLLARESGPS
    def get_Unidadesgps(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM unidad_gps")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    "id": int(data[0]),
                    "numero_serie": data[1],
                    "nivel_bateria": data[2],
                    "fecha_hora_ultimo_reporte": data[3],
                    "id_ciego_vinculado": int(data[4]),
                    'estado': bool(data[5]),
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="UnidadesGPS not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # ACTUALIZAR COLLARGPS
    def update_gps(self, gps_id: int, dispositivo_gps: Dispositivo_GPS):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE unidad_gps SET numero_serie = %s, nivel_bateria = %s, fecha_hora_ultimo_reporte = %s, id_ciego_vinculado=%s, estado = %s WHERE id = %s",
                           (dispositivo_gps.numero_serie, dispositivo_gps.nivel_bateria, dispositivo_gps.fecha_hora_ultimo_reporte, dispositivo_gps.id_ciego_vinculado, dispositivo_gps.estado, gps_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="GPS not found")
            return {"mensaje": "Datos del GPS actualizados exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    # ELIMINAR COLLARGPS
    def delete_gps(self, gps_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM unidad_gps WHERE id = %s",
                           (gps_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="GPS no encontrado")
            return {"mensaje": "GPS eliminado exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    # FIN COLLARGPS
