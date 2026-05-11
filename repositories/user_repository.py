

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel


class UserRepository:
    def __init__(self, db:AsyncSession):
        self.db = db


    async def get_user_by_username(self, username: str):
        result = await self.db.execute(select(UserModel).filter_by(username=username))
        return result.scalar()




    async def create_user(self, username: str, password: str):
        user = UserModel(username=username, hashed_password=password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user