from uuid import UUID

from app.repo.schemas.student_schemas.add_new_student_schemas import AddNewStudentSchemas, StudentInfoSchemas
from ...dependecy import AsyncSession
from sqlalchemy import select
from ...models import StudentsModel

class StudentQueries:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def get_user_info(self, id:UUID):
        res = await self.session.execute(select(StudentsModel).where(StudentsModel.id == UUID(id)))
        output = res.scalar_one_or_none()
        
        if not output:
            return None
        
        return StudentInfoSchemas(
            fullName=output.full_name,
            identifier=output.identifier,
            classId=output.class_id,
            id = output.id
        )