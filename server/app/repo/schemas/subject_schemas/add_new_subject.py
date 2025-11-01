from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel, UUID4


T = TypeVar("T")

class AddNewSubjectSchemas(BaseModel):
    title: str
    author: str
    enable: bool
    classId: UUID4


class ParticularSubjectSchemas(BaseModel):
    id: UUID4
    title: str
    author: str
    enable: bool
    classId: UUID4



class SubjectInfoSchemas(BaseModel, Generic[T]):
    className: str
    teacherName: str
    classId: UUID4
    subjects: Optional[List[T]] = None


class SubjectById(BaseModel):
    classId: UUID4
