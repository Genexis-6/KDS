from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.repo.schemas.default_server_res import DefaultServerApiRes
from app.repo import db_injection
from app.repo.queries.class_room_queries.class_queries import ClassQueries
from app.repo.schemas.class_schemas.add_new_class_schemas import AddNewClassSchemas
from app.utils.enums.class_room_enums import ClassRoomEnums
from typing import List
from app.repo.schemas.class_schemas.class_schemas import ClassSchemas



room = APIRouter(
    tags=['class'],
    prefix="/class",
    responses={
        404:{
            "message": "not found"
        }
    }
)


@room.get("/all_classess", response_model=DefaultServerApiRes[List[ClassSchemas]])
async def get_all_available_class(db: db_injection):
    class_ =  ClassQueries(db)
    all_classes = await class_.get_all_classes()
    return DefaultServerApiRes(
        statusCode=200,
        message="all available class",
        data=all_classes
    )
    
  

@room.post("/add_class", response_model=DefaultServerApiRes)
async def add_new_class(db: db_injection, add:AddNewClassSchemas):
    class_ =  ClassQueries(db)
    add_class = await class_.add_new_class(add)
    if add_class == ClassRoomEnums.EXIST:
        return JSONResponse(
            content={"message":"class room already exist"},
            status_code= 400
        )
    return DefaultServerApiRes(
        statusCode=200,
        message=f"{add.class_name} has been created"
    )
    