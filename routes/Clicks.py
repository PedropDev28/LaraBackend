from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Clicks import Clicks

router = APIRouter()

@router.get("/", response_model=List[Clicks])
async def get_clicks():
    clicks = await db["clicks"].find().to_list(100)
    return clicks

@router.post("/", response_model=Clicks)
async def create_clicks(clicks: Clicks):
    result = await db["clicks"].insert_one(clicks.model_dump(by_alias=True))
    clicks.id = str(result.inserted_id)
    return clicks

@router.get("/{clicks_id}", response_model=Clicks)
async def get_clicks(clicks_id: str):
    clicks = await db["clicks"].find_one({"_id": ObjectId(clicks_id)})
    if not clicks:
        raise HTTPException(status_code=404, detail="Click no encontrado")
    return clicks

@router.put("/{clicks_id}", response_model=Clicks)
async def update_clicks(clicks_id: str, clicks: Clicks):
    result = await db["clicks"].update_one(
        {"_id": ObjectId(clicks_id)}, {"$set": clicks.model_dump(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Click no encontrado")
    clicks.id = clicks_id
    return clicks

@router.delete("/{clicks_id}")
async def delete_clicks(clicks_id: str):
    result = await db["clicks"].delete_one({"_id": ObjectId(clicks_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Click no encontrado")
    return {"message": "Click eliminado"}