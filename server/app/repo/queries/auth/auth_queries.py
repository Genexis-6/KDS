
from app.utils.enums.class_room_enums import ClassRoomEnums
from app.repo.schemas.student_schemas.add_new_student_schemas import AddNewStudentSchemas
from app.utils.enums.auth_enums import AuthEums
from app.security.password_hasher import generate_password, verify_hash_password
from app.repo.schemas.login_schemas import LoginUserSchemas

from ...dependecy import AsyncSession
from sqlalchemy import select
from ...models import StudentsModel, AdminModel

from uuid import uuid4



class AuthQueries:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def check_student_exist(self, identifier: str):
        res = await self.session.execute(select(StudentsModel).where(StudentsModel.identifier == identifier))
        output = res.scalar_one_or_none()
        return output
        
    async def check_admin_exist(self, identifier: str):
        res = await self.session.execute(select(AdminModel).where(AdminModel.identifier == identifier))
        output = res.scalar_one_or_none()
        return output

    
    async def add_new_student(self, add:AddNewStudentSchemas):
        check = await self.check_student_exist(add.identifier)
        if check:
            return AuthEums.EXISTS
        self.session.add(
            StudentsModel(
               id=uuid4(),
               class_id=add.class_id,
               full_name=add.full_name,
               identifier=add.identifier,
               password = generate_password(add.password)
            )
        )
        await self.session.commit()
        return AuthEums.CREATED
    
    
    
    async def login_user(self, login: LoginUserSchemas):
        if login.role == "admin":
            user = await self.check_admin_exist(identifier=login.identifier)
        else:
            user = await self.check_student_exist(login.identifier)
        if user:
            if verify_hash_password(login.password, hash_pass=user.password):
                return user
            return AuthEums.NOT_ALLOWED
        return AuthEums.NOT_FOUND