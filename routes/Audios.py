from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Audios import Audios

router = APIRouter()

@router.get("/", response_model=List[Audios])
async def get_audios():
    audios = await db["audios"].find().to_list(15000)
    return audios

@router.get("/by_user/{user_mail}", response_model=List[Audios])
async def get_audios_by_user(user_mail: str):
    audios = await db["audios"].find({"usuario.mail": user_mail}).to_list(100)
    return audios

@router.get("/twenty_audios", response_model=List[Audios])
async def get_twenty_audios():
    audios = await db["audios"].find().to_list(20)
    return audios


@router.get("/five_less", response_model=List[Audios])
async def get_five_less_audios():
    ##hacer pipeline para sacar los 5 tags menos usados
    pipeline = [
        # Contamos cuántas veces aparece cada tag
        {"$group": {"_id": "$texto.tag", "cantidad": {"$sum": 1}}},  
        # Ordenamos de menor a mayor cantidad de uso
        {"$sort": {"cantidad": 1}},  
        # Limitamos a los 5 menos usados
        {"$limit": 5},  
        # Hacemos un lookup para traer los audios completos con esos tags
        {
            "$lookup": {
                "from": "audios",
                "localField": "_id",
                "foreignField": "texto.tag",
                "as": "audios_completos"
            }
        },  
        # Desanidamos la lista de audios y tomamos solo uno por cada tag menos usado
        {"$unwind": "$audios_completos"},
        # Agrupamos de nuevo para devolver los audios completos
        {
            "$replaceRoot": {
                "newRoot": "$audios_completos"
            }
        }
    ]

    audios = await db["audios"].aggregate(pipeline).to_list(5)
    return audios


@router.get("/five_random", response_model=List[Audios])
async def get_five_random_audios():
    pipeline = [
    {"$sample": {"size": 5}}
    ]
    audios = await db["audios"].aggregate(pipeline).to_list(5)
    return audios

@router.post("/", response_model=Audios)
async def create_audios(audios: Audios):
    result = await db["audios"].insert_one(audios.dict(by_alias=True))
    audios.id = str(result.inserted_id)
    return audios

@router.get("/{audios_id}", response_model=Audios)
async def get_audios(audios_id: str):
    audios = await db["audios"].find_one({"_id": ObjectId(audios_id)})
    if not audios:
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    return audios

@router.put("/{audios_id}", response_model=Audios)
async def update_audios(audios_id: str, audios: Audios):
    result = await db["audios"].update_one(
        {"_id": ObjectId(audios_id)}, {"$set": audios.dict(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    audios.id = audios_id
    return audios

@router.get("/search", response_model=List[Audios])
async def search_audios_by_text(text: str):
    audios = await db["audios"].find({"texto": {"$regex": text, "$options": "i"}}).to_list(100)
    if not audios:
        raise HTTPException(status_code=404, detail="No se encontraron audios")
    return audios

@router.delete("/{audios_id}")
async def delete_audios(audios_id: str):
    result = await db["audios"].delete_one({"_id": ObjectId(audios_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    return {"message": "Audios eliminado"}