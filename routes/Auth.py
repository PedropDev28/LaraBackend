from fastapi.responses import JSONResponse
import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Request
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from models.Usuario import Usuario


router = APIRouter()

# Clave secreta para firmar el token
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# Función para generar el token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para generar el hash de la contraseña	
def generate_password(password: str):
    return generate_password_hash(password)

# Ruta para iniciar sesión y obtener el token
@router.post("/token")
async def login_for_access_token(form_data: dict):
    # Buscar usuario en la base de datos por su correo
    user = await db["usuarios"].find_one({"mail": form_data['username']})
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verificar la contraseña
    if not check_password_hash(user["password"], form_data['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Crear token si la autenticación es exitosa
    user_dict = {"username": form_data['username']}
    token = create_access_token(data=user_dict)
    
    response = JSONResponse(content={"message": "Login successful", "token": token})
    
    return response

# Dependencia para obtener el usuario del token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=credentials_exception)
    except jwt.PyJWTError:
        raise HTTPException(status_code=credentials_exception)
    return username

# Ruta para cerrar sesión
@router.get("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("access_token")
    return response



# Ruta para registrar un usuario
@router.post("/register")
async def register_user(form_data: dict):
    user = await db["usuarios"].find_one({"mail": form_data['mail']})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    raw_fecha_nacimiento = form_data.get('fecha_nacimiento')
    try:
        if isinstance(raw_fecha_nacimiento, dict) and '$date' in raw_fecha_nacimiento:
            fecha_nacimiento = datetime.fromisoformat(raw_fecha_nacimiento['$date'].replace('Z', '+00:00'))
        else:
            fecha_nacimiento = datetime.fromisoformat(raw_fecha_nacimiento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid fecha_nacimiento format: {e}")
    
    new_user = Usuario(
        mail=form_data['mail'],
        password=generate_password(form_data['password']),
        rol="cliente",
        nombre=form_data['nombre'],
        sexo=form_data['sexo'],
        parent=form_data['parent'],
        provincia=form_data['provincia'],
        enfermedades=form_data['enfermedades'],
        dis=form_data['dis'],
        font_size=form_data['font_size'],
        entidad=form_data['entidad'],
        observaciones=form_data['observaciones'],
        ultima_conexion=datetime.now(),
        cant_audios=form_data['cant_audios'],
        fecha_nacimiento=fecha_nacimiento
    )
    
    user_dict = new_user.dict()

    await db["usuarios"].insert_one(user_dict)
    return {"message": "User registered successfully"}