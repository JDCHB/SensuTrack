import mysql.connector
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.ciego_model import *
from app.models.ciego_map_model import CiegosMap
from fastapi.encoders import jsonable_encoder


class CiegoController():
    
    def Ciegos_Map(self, ciegosmap: CiegosMap):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT 
                    d.nombre AS nombre_discapacitado, 
                    c.latitud, 
                    c.longitud, 
                    cgps.numero_serie, 
                    cgps.nivel_bateria
                FROM 
                    ciegos d
                JOIN 
                    coordenada c ON d.id = c.id_ciego
                LEFT JOIN 
                    unidad_gps cgps ON cgps.id_ciego_vinculado = d.id
                WHERE 
                    d.id_cuidador = %s
                ORDER BY 
                    d.nombre, c.create_f DESC
                LIMIT 25;
                """,
                (ciegosmap.user_id,)
            )
            result = cursor.fetchall()
            payload = []

            # Recorremos cada fila de los resultados
            for data in result:
                content = {
                    'nombre_discapacitado': data[0],
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
                    status_code=404, detail="El Discapacitado no ha sido encontrado para el usuario"
                )

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, detail="Error en la base de datos")

        finally:
            conn.close()

        # CIEGOS REPORTE
    def Ciegos_Report(self, ciegosreporte: CiegosReporte):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT
                    ciegos.id AS id_discapacitado,
                    ciegos.nombre,
                    genero.genero AS genero,
                    tipo.tp_ceguera AS tipo_ceguera,
                    cuidador.nombre AS nombre_cuidador,
                    ciegos.fecha,
                    ciegos.estado AS reporte_discapacitados
                FROM
                    ciegos
                INNER JOIN
                    genero_discapacitado AS genero ON ciegos.id_genero_discapacitado = genero.id
                INNER JOIN
                    tipo_ceguera AS tipo ON ciegos.id_tipo_ceguera = tipo.id
                INNER JOIN
                    usuarios AS cuidador ON ciegos.id_cuidador = cuidador.id
                WHERE
                    ciegos.fecha BETWEEN %s AND %s
                LIMIT 25;
                """, (ciegosreporte.fecha1, ciegosreporte.fecha2))
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': str(data[1]),
                    'genero': str(data[2]),
                    'tipo_ceguera': str(data[3]),
                    'nombre_cuidador': str(data[4]),
                    'fecha': data[5],
                    'estado': bool(data[6]),
                }
                payload.append(content)
                content = {}
                
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Ciego not found")

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Database error")
    
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
        finally:
            conn.close()

    # CREAR DISCAPACITADO
    def create_discapacitadoV(self, discapacitadov: DiscapacitadoV):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ciegos (nombre,id_genero_discapacitado,id_tipo_ceguera,id_cuidador,estado) VALUES (%s, %s, %s, %s, %s)",
                           (discapacitadov.nombre, discapacitadov.id_genero_discapacitado, discapacitadov.id_tipo_ceguera, discapacitadov.id_cuidador, discapacitadov.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Discapacitado Registrado"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # BUSCAR DISCAPACITADO
    def get_discapacitadoV(self, discapacitado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM ciegos WHERE id = %s", (discapacitado_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                "id": int(result[0]),
                "nombre": result[1],
                "id_genero_discapacitado": int(result[2]),
                "id_tipo_ceguera": int(result[3]),
                "id_cuidador": int(result[4]),
                'estado': bool(result[5]),
            }
            payload.append(content)

            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(
                    status_code=404, detail="Discapacitado not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # VER TODOS LOS DISCAPACITADOS
    def get_discapacitadosV(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ciegos")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'id_genero_discapacitado': int(data[2]),
                    'id_tipo_ceguera': int(data[3]),
                    'id_cuidador': int(data[4]),
                    'estado': bool(data[5]),
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Discapacitado not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # VER TODOS LOS DISCAPACITADOS
    def get_discapacitadosV_SIN_GPS(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.* 
                FROM ciegos c
                LEFT JOIN unidad_gps u ON c.id = u.id_ciego_vinculado
                WHERE u.id_ciego_vinculado IS NULL
            """)
            result = cursor.fetchall()
            payload = []
            
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'id_genero_discapacitado': int(data[2]),
                    'id_tipo_ceguera': int(data[3]),
                    'id_cuidador': int(data[4]),
                    'estado': bool(data[5]),
                }
                payload.append(content)

            json_data = jsonable_encoder(payload)
            
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="No hay discapacitados sin GPS asignado")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # ACTUALIZAR DISCAPACITADO
    def update_discapacitadoV(self, discapacitado_id: int, discapacitadov: DiscapacitadoV):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE ciegos SET nombre = %s, id_genero_discapacitado = %s, id_tipo_ceguera = %s, id_cuidador = %s, estado = %s WHERE id = %s",
                           (discapacitadov.nombre, discapacitadov.id_genero_discapacitado, discapacitadov.id_tipo_ceguera, discapacitadov.id_cuidador, discapacitadov.estado, discapacitado_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Discapacitado not found")
            return {"mensaje": "Datos del Discapacitado actualizado exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    # ELIMINAR DISCAPACITADO
    def delete_discapacitadoV(self, discapacitado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM ciegos WHERE id = %s", (discapacitado_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Discapacitado no encontrado")
            return {"mensaje": "Discapacitado eliminado exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

