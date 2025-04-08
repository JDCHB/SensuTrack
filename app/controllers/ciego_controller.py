import mysql.connector
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.ciego_model import *
from app.models.ciego_map_model import *
from fastapi.encoders import jsonable_encoder


class CiegoController():
    
    def Ciegos_Map(self, ciegosmap: CiegosMap):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT 
                    d.id,
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
                    'id': data[0],
                    'nombre_discapacitado': data[1],
                    'latitud': data[2],
                    'longitud': data[3],
                    'numero_serie': data[4],
                    'nivel_bateria': data[5]
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

    #CREATE ZONAS SEGURAS
    def create_Zona_Segura(self, ciegozonas: CiegoZonaS):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO zonas_seguras (nombre_zona, latitud, longitud, radio, id_discapacitado, estado) VALUES (%s, %s, %s, %s, %s)",
                           (ciegozonas.nombre_zona, ciegozonas.latitud, ciegozonas.longitud, ciegozonas.radio, ciegozonas.id_discapacitado, ciegozonas.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Zona Segura Registrada Exitosamente"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    #GET ZONAS SEGURAS POR DISCAPACITADO
    def get_Zona_Segura(self, zona_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT 
                    zs.id, 
                    zs.nombre_zona, 
                    zs.latitud, 
                    zs.longitud,
                    zs.radio,
                    zs.id_discapacitado,
                    zs.estado
                FROM zonas_seguras AS zs 
                WHERE id_discapacitado = %s""", (zona_id,))
            
            results = cursor.fetchall()
            payload = []

            for row in results:
                content = {
                    "id": int(row[0]),
                    "nombre_zona": row[1],
                    "latitud": row[2],
                    "longitud": row[3],
                    "radio": float(row[4]),
                    "id_discapacitado": int(row[5]),
                    'estado': bool(row[6]),
                }
                payload.append(content)

            if results:
                return jsonable_encoder(payload)
            else:
                raise HTTPException(status_code=404, detail="Zonas seguras no encontradas")

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    # ACTUALIZAR ZONA SEGURA
    def update_Zona_Segura(self, zona_id: int, ciegozonas: CiegoZonaSUPDATE):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE zonas_seguras SET nombre_zona = %s, latitud = %s, longitud = %s, radio = %s WHERE id = %s",
                           (ciegozonas.nombre_zona, ciegozonas.latitud, ciegozonas.longitud, ciegozonas.radio, zona_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Zona Segura not found")
            return {"mensaje": "La Zona Segura fue actualizada exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()


    def delete_Zona_Segura(self, zona_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM zonas_seguras WHERE id = %s", (zona_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Zona Segura no encontrada")
            return {"mensaje": "Zona Segura eliminada exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

    
    def update_estado_Zona_Segura(self, zona_id: int, ciegozonas: CiegoZonaSESTADO):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE zonas_seguras SET estado = %s WHERE id = %s",
                    (ciegozonas.estado, zona_id,)
                )
                conn.commit()

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404, detail="Zona Segura no encontrada")

                return {"mensaje": "Estado de la zona segura actualizada exitosamente"}

            except mysql.connector.Error as err:
                raise HTTPException(status_code=500, detail=str(err))

            finally:
                if conn:
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

    # EN ESTE SE VEN TODOS LOS DISCAPACITADOS PERO CON SUS DATOS MAS NO CON SUS ID
    def get_discapacitadosVCOMPLETOS(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT
                    ciegos.id AS id_discapacitado,
                    ciegos.nombre,
                    genero.genero AS genero,
                    tipo.tp_ceguera AS tipo_ceguera,
                    cuidador.nombre AS nombre_cuidador,
                    ciegos.estado AS estado
                FROM
                    ciegos
                INNER JOIN
                    genero_discapacitado AS genero ON ciegos.id_genero_discapacitado = genero.id
                INNER JOIN
                    tipo_ceguera AS tipo ON ciegos.id_tipo_ceguera = tipo.id
                INNER JOIN
                    usuarios AS cuidador ON ciegos.id_cuidador = cuidador.id
                LIMIT 25;
                """)
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'genero': data[2],
                    'tipo_ceguera': data[3],
                    'nombre_cuidador': data[4],
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

    def update_estado_discapacitado(self, discapacitado_id: int, discapacitadoestado: DiscapacitadoEstado):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE ciegos SET estado = %s WHERE id = %s",
                    (discapacitadoestado.estado, discapacitado_id,)
                )
                conn.commit()

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404, detail="Discapacitado no encontrado")

                return {"mensaje": "Estado del Discapacitado actualizado exitosamente"}

            except mysql.connector.Error as err:
                raise HTTPException(status_code=500, detail=str(err))

            finally:
                if conn:
                    conn.close()