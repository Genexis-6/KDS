from pydantic import BaseModel, UUID4


class AddNewStudentSchemas(BaseModel):
    full_name:str
    identifier:str
    class_id:UUID4
    password:str