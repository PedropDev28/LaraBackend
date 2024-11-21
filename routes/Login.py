from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db import db
from models.Login import Login

router = APIRouter()


# @router.post("/")
# async def login(login_data: Login):
#     usuario = await db["usuarios"].find_one({"mail": login_data.email, "password": login_data.password})
#     if not usuario:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
#     return {"email": usuario["mail"], "nombre": usuario["nombre"], "message": "Inicio de sesión exitoso"}

@router.post("/")
async def login_for_access_token(form_data: dict):
    user_dict = {"username": form_data['username']}
    token = create_access_token(data=user_dict)
    
    response = JSONResponse(content={"message": "Login successful"})
    
    # Setea el token en la cookie
    response.set_cookie(
        "access_token", 
        token, 
        httponly=True, 
        secure=True,
        samesite="Strict", 
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return response