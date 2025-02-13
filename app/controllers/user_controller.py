import mysql.connector

##captcha
import requests
##SOLO ESO
from fastapi import HTTPException, UploadFile
import pandas as pd
from app.config.db_config import get_db_connection
from app.models.user_model import User, Login, Token, UserEstado, UPDATE_User
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "PetTrackerOF"

# Clave secreta de reCAPTCHA (debes obtenerla de Google)
RECAPTCHA_SECRET_KEY = "6Lf0vdUqAAAAAIT2ro4eRfRxaCjleAdWSpCRso27"

class Usercontroller():

    
    #VERIFICACION DEL CAPTCHA
    async def verify_recaptcha(recaptcha_token: str):
        """Verifica el token del Captcha con Google reCAPTCHA"""
        url = "https://www.google.com/recaptcha/api/siteverify"
        data = {
            "secret": RECAPTCHA_SECRET_KEY,
            "response": recaptcha_token
        }
        response = requests.post(url, data=data)
        result = response.json()

        if not result.get("success"):
            raise HTTPException(status_code=400, detail="Captcha inválido o fallido")



    # CREAR TOCKEN
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
            to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    # GENERAR EL TOKEN

    async def login_generate_token(self, user: Login):
        try:

            # Verificar Captcha antes de validar credenciales
            await verify_recaptcha(recaptcha_token)

            conn = get_db_connection()
            cursor = conn.cursor()

            # Consulta para validar usuario y obtener sus datos
            cursor.execute(
                "SELECT id, email, password, id_rol FROM usuarios WHERE email = %s AND password = %s",
                (user.email, user.password)
            )
            result = cursor.fetchone()

            if result:
                # Generar token
                access_token_expires = timedelta(minutes=60)
                access_token = self.create_access_token(
                    # Usa el email como "sub" en el token
                    data={"sub": result[1]},
                    expires_delta=access_token_expires
                )

                # Preparar los datos del usuario
                user_data = {
                    "id": result[0],
                    "email": result[1],
                    "id_rol": result[3]
                }

                # Retornar token y datos del usuario
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    # Convertir a JSON seguro
                    "user_data": jsonable_encoder(user_data)
                }
            else:
                raise HTTPException(
                    status_code=401, detail="Credenciales incorrectas")

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, detail="Error interno en la base de datos")
        finally:
            conn.close()

    # VERIFICAR EL TOKEN

    async def verify_token(self, token: Token):

        try:
            payload = jwt.decode(token.token, SECRET_KEY, algorithms=["HS256"])
            return {"message": "Token válido"}
        except jwt.ExpiredSignatureError:
            return {"message": "Token expirado"}
        except jwt.InvalidTokenError:
            return {"message": "Token inválido"}

    # LOGIN

    def login(self, user: Login):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, email, password, id_rol FROM usuarios WHERE email = %s AND password = %s", (user.email, user.password))
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': data[0],
                    'email': data[1],
                    'password': data[2],
                    'id_rol': data[3]
                    # 'nombre': data[3],
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # Cargue Masivo

    def create_usuario_masivo(self, file: UploadFile):
        conn = None
        try:
            # Leer el archivo Excel
            df = pd.read_excel(file.file, engine='openpyxl')

            required_columns = ['email', 'password',
                                'nombre', 'apellido', 'documento', 'telefono', 'id_rol']
            for col in required_columns:
                if col not in df.columns:
                    return {"error": f"Falta la columna: {col}"}

            # Conectar a la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()

            for index, row in df.iterrows():
                cursor.execute("INSERT INTO usuarios (email,password,nombre,apellido,documento,telefono,id_rol,estado) VALUES (%s, %s, %s, %s, %s, %s ,%s ,%s)",
                               (row['email'], row['password'],
                                row['nombre'], row['apellido'], row['documento'], row['telefono'], row['id_rol'], row['estado'])
                               )

            conn.commit()  # Hacer commit después de todas las inserciones
            return {"resultado": "Usuarios creados exitosamente"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()  # Asegúrate de que conn esté definido
            return {"error": str(err)}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": f"Un error inesperado ocurrió: {str(e)}"}
        finally:
            if conn:
                conn.close()

    # HASTA AQUI

    # CREAR USUARIO
    def create_user(self, user: User):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (email,password,nombre,apellido,documento,telefono,id_rol,estado) VALUES (%s, %s, %s, %s, %s, %s ,%s ,%s)",
                           (user.email, user.password, user.nombre, user.apellido, user.documento, user.telefono, user.id_rol, user.estado))
            conn.commit()
            conn.close()
            return {"resultado": "Usuario creado"}
        except mysql.connector.Error as err:
            conn.rollback()
            return {"error": f"Error al crear usuario: {err}"}
        finally:
            if conn:
                conn.close()

    # BUSCAR USUARIO
    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            payload = []
            content = {}

            content = {
                'id': int(result[0]),
                'email': result[1],
                'password': result[2],
                'nombre': result[3],
                'apellido': result[4],
                'documento': result[5],
                'telefono': result[6],
                'id_rol': int(result[7]),
                'estado': bool(result[8])
            }
            payload.append(content)

            json_data = jsonable_encoder(content)
            if result:
                return json_data
            else:
                raise HTTPException(status_code=404, detail="User not found")

        except mysql.connector.Error as err:
            conn.rollback()
            return {"error": f"Database error: {err}"}
        finally:
            if conn:
                conn.close()

    # VER USUARIOS
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'id': int(data[0]),
                    'email': data[1],
                    'password': data[2],
                    'nombre': data[3],
                    'apellido': data[4],
                    'documento': data[5],
                    'telefono': data[6],
                    'id_rol': int(data[7]),
                    'estado': bool(data[8])
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")

        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    # ACTUALIZAR USUARIO
    def update_user(self, user_id: int, user: UPDATE_User):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET email = %s, nombre = %s, apellido = %s, documento = %s, telefono = %s, estado = %s WHERE id = %s",
                (user.email, user.nombre, user.apellido,
                 user.documento, user.telefono, user.estado, user_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")

            return {"mensaje": "Usuario actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()

    # ACTUALIZAR ESTADO USUARIO
    def update_estado_user(self, user_id: int, user: UserEstado):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET estado = %s WHERE id = %s",
                (user.estado, user_id,)
            )
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")

            return {"mensaje": "Estado de Usuario actualizado exitosamente"}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

        finally:
            if conn:
                conn.close()

    # ELIMINAR USARIO
    def delete_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")
            return {"mensaje": "Usuario eliminado exitosamente"}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()

# FIN DE LA CLASE USUARIO
