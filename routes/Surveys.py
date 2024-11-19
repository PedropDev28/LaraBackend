from fastapi import APIRouter, HTTPException
from db import db
from bson import ObjectId
from typing import List
from models.Surveys import Surveys

router = APIRouter()

@router.get("/", response_model=List[Surveys])
async def get_surveys():
    surveys = await db["surveys"].find().to_list(100)
    return surveys

@router.post("/", response_model=Surveys)
async def create_surveys(surveys: Surveys):
    result = await db["surveys"].insert_one(surveys.model_dump(by_alias=True))
    surveys.id = str(result.inserted_id)
    return surveys

@router.get("/{surveys_id}", response_model=Surveys)
async def get_surveys(surveys_id: str):
    surveys = await db["surveys"].find_one({"_id": ObjectId(surveys_id)})
    if not surveys:
        raise HTTPException(status_code=404, detail="Survey no encontrada")
    return surveys

@router.put("/{surveys_id}", response_model=Surveys)
async def update_surveys(surveys_id: str, surveys: Surveys):
    result = await db["surveys"].update_one(
        {"_id": ObjectId(surveys_id)}, {"$set": surveys.model_dump(by_alias=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Survey no encontrada")
    surveys.id = surveys_id
    return surveys

@router.delete("/{surveys_id}")
async def delete_surveys(surveys_id: str):
    result = await db["surveys"].delete_one({"_id": ObjectId(surveys_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Survey no encontrada")
    return {"message": "Survey eliminada"}