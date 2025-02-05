import mysql.connector
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.admin_model import NuevoCollar, NuevoModulo, Actualizar_Estado_Modulo, ModuloxRol
from fastapi.encoders import jsonable_encoder


class AdminController():

    # CREAR NUEVO COLLAR GPS
    def create_collar(self, nuevocollar: NuevoCollar):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verifica si el número de serie ya existe
            cursor.execute(
                "SELECT id FROM collares_con_gps WHERE numero_serie = %s", (nuevocollar.numero_serie,))
            if cursor.fetchone():
                return {"error": "El número de serie ya está registrado."}

            # Inserta el nuevo collar
            cursor.execute(
                """
                INSERT INTO collares_con_gps (numero_serie, id_mascota_vinculada, nivel_bateria, estado)
                VALUES (%s, %s, %s, %s)
                """,
                (nuevocollar.numero_serie,
                 nuevocollar.id_mascota_vinculada, nuevocollar.nivel_bateria, nuevocollar.estado)
            )
            conn.commit()
            return {"resultado": "Collar registrado exitosamente"}

        except mysql.connector.Error as err:
            conn.rollback()
            return {"error": f"Error en la base de datos: {err}"}

        finally:
            conn.close()

    # CREAR MODULO

    def create_modulo(self, nuevomodulo: NuevoModulo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO modulo (nombre, descripcion, ubicacion, estado) VALUES (%s, %s, %s, %s)",
                           (nuevomodulo.nombre, nuevomodulo.descripcion, nuevomodulo.ubicacion, nuevomodulo.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Modulo creado"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # BUSCAR MODULO

    def get_modulo(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulo WHERE id = %s", (modulo_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                'id': int(result[0]),
                'nombre': result[1],
                'descripcion': result[2],
                'ubicacion': result[3],
                'estado': bool(result[4])
            }
            payload.append(content)

            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Modulo not found")

        except mysql.connector.Error as err:
            conn.rollback()
            return {"error": f"Database error: {err}"}
        finally:
            if conn:
                conn.close()

    # VER MODULOS

    def get_modulos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulo")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'descripcion': data[2],
                    'ubicacion': data[3],
                    'estado': bool(data[4])
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Modulos not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # ACTUALIZAR MODULOS
    def update_modulo(self, modulo_id: int, nuevomodulo: NuevoModulo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE modulo SET nombre = %s, descripcion = %s, ubicacion=%s, estado = %s WHERE id = %s",
                (nuevomodulo.nombre, nuevomodulo.descripcion,
                 nuevomodulo.estado, modulo_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Modulo no encontrado")

            return {"mensaje": "Modulo actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()

    # ACTUALIZAR ESTADO DEL MODULO
    def update_estado_modulo(self, modulo_id: int, actualizar_estado_modulo: Actualizar_Estado_Modulo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE modulo SET estado = %s WHERE id = %s",
                (actualizar_estado_modulo.estado, modulo_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Modulo no encontrado")

            return {"mensaje": "Estado de Modulo actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()

    # DESDE AQUI ES MODULOXROL

    # def create_moduloXrol(self, moduloxrol: ModuloxRol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO moduloxrol (id_modulo, id_rol, estado) VALUES(%s, %s, %s)",
                           (moduloxrol.id_modulo, moduloxrol.id_rol, moduloxrol.estado))
            conn.commit()
            conn.close()
            return {"resultado": "ModuloXrol creado"}
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    def create_moduloXrol(self, moduloxrol: ModuloxRol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            print("moduloxperfilssssssssssssssssssssssssssssss")
            cursor.execute("SELECT id from modulo")
            rv = cursor.fetchall()

            print(moduloxrol)

            for result in rv:
                id_modulo_v = result[0]
                print("-------------------------------------------1", result)
                cursor.execute("INSERT INTO moduloxrol (id_rol,id_modulo,estado) VALUES (%s,%s,%s)", (
                    moduloxrol.id_rol, id_modulo_v, 0,))
                conn.commit()

            for result in moduloxrol.id_modulo:
                print("-------------------------------------------2", result)
                cursor.execute("""
                             UPDATE moduloxrol AS mx
                            SET estado = 1
                            WHERE id_rol = %s AND id_modulo=%s   
                        """, (moduloxrol.id_rol, result))
                conn.commit()
            conn.close()
            id = cursor.lastrowid
            return {id}  # aja

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    def get_moduloXrol(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulo WHERE id = %s", (modulo_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                'id': int(result[0]),
                'nombre': result[1],
                'descripcion': result[2],
                'estado': bool(result[3])
            }
            payload.append(content)

            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Modulo not found")

        except mysql.connector.Error as err:
            conn.rollback()
            return {"error": f"Database error: {err}"}
        finally:
            if conn:
                conn.close()

    # VER MODULOS

    def get_modulosXrol(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulo")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'nombre': data[1],
                    'descripcion': data[2],
                    'estado': bool(data[3])
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Modulos not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # ACTUALIZAR MODULOS
    def update_moduloXrol(self, modulo_id: int, nuevomodulo: NuevoModulo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE modulo SET nombre = %s, descripcion = %s, estado = %s WHERE id = %s",
                (nuevomodulo.nombre, nuevomodulo.descripcion,
                 nuevomodulo.estado, modulo_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Modulo no encontrado")

            return {"mensaje": "Modulo actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()

    # ACTUALIZAR ESTADO DEL MODULO
    def update_estado_moduloXrol(self, modulo_id: int, actualizar_estado_modulo: Actualizar_Estado_Modulo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE modulo SET estado = %s WHERE id = %s",
                (actualizar_estado_modulo.estado, modulo_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Modulo no encontrado")

            return {"mensaje": "Estado de Modulo actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()
