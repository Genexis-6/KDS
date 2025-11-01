from app.repo.schemas.class_schemas.add_new_class_schemas import AddNewClassSchemas
from app.utils.enums.class_room_enums import ClassRoomEnums
from app.repo.schemas.class_schemas.class_schemas import ClassSchemas
from ...dependecy import AsyncSession
from sqlalchemy import UUID, select
from ...models import ClassModel
from uuid import uuid4



class ClassQueries:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def check_class_exist(self, class_name: str):
        res = await self.session.execute(select(ClassModel).where(ClassModel.class_name == class_name))
        output = res.scalar_one_or_none()
        return output
    
    async def get_class_by_id(self, id: UUID):
        res = await self.session.execute(select(ClassModel).where(ClassModel.id == id))
        output = res.scalar_one_or_none()
        if output is None:
            return None
        return ClassSchemas(
            id=output.id,
            className=output.class_name,
            teacherName=output.teacher_name
        )
        
    async def get_all_classes(self):
        res = await self.session.execute(select(ClassModel))
        output = res.scalars().all()
        return [
            ClassSchemas(
                className=dt.class_name,
                teacherName=dt.teacher_name,
                id=dt.id
            )
            for dt in output
            
            ] if not None else []
    
    
    async def add_new_class(self, add:AddNewClassSchemas):
        check = await self.check_class_exist(add.class_name)
        if check:
            return ClassRoomEnums.EXIST
        self.session.add(
            ClassModel(
                id = uuid4(),
                class_name= add.class_name,
                teacher_name= add.teacher_name
            )
        )
        await self.session.commit()
        return ClassRoomEnums.CREATED