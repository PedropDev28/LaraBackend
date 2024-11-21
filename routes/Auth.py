from fastapi.responses import JSONResponse
import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Request


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

# Ruta para iniciar sesión y obtener el token
@router.post("/token")
async def login_for_access_token(form_data: dict):
    # Aquí haces la autenticación real, validando un usuario y una contraseña
    user_dict = {"username": form_data['username']}
    token = create_access_token(data=user_dict)
    
    response = JSONResponse(content={"message": "Login successful"})
    
    # Setea el token en la cookie
    response.set_cookie(
        "access_token", 
        token, 
        httponly=True, 
        secure=True,  # Solo en HTTPS
        samesite="Strict", 
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
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

@router.get("/protected")
async def protected_route(request: Request):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        user = get_current_user(token)
        return {"message": f"Hello {user}"}
    except HTTPException as e:
        raise e