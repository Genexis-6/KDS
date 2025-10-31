from pydantic import BaseModel, UUID4


class ClassSchemas(BaseModel):
    id:UUID4
    className:str
    teacherName:str