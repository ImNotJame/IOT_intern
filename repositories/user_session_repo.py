from datetime import datetime

import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from models.user_session_model import UserSessionModel


class UserSessionRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create_user_session(self, user_id: int,
                                  jwt_token: str,
                                  refresh_token: str,
                                  login_time: datetime = datetime.now(tz=pytz.timezone('Asia/Bangkok')),
                                  flag: bool = True):
        await self.db.execute(
                update(UserSessionModel)
                .where(UserSessionModel.user_id == user_id, UserSessionModel.user_flag == True)
                .values(user_flag=False, user_logout_time=datetime.now(tz=pytz.timezone('Asia/Bangkok')))
        )

        user_session = UserSessionModel(user_id=user_id,
                                        user_jwt_token=jwt_token,
                                        user_refresh_token=refresh_token,
                                        user_login_time=login_time,
                                        user_flag=flag)
        self.db.add(user_session)
        await self.db.commit()
        await self.db.refresh(user_session)
        return user_session

    async def get_active_user_session_by_user_id(self, user_id: int):
        result = await self.db.execute(select(UserSessionModel).filter_by(user_id=user_id, user_flag=True))
        return result.scalar()

    async def delete_user_session_by_user_id(self, user_id: int):
        user_session = await self.get_active_user_session_by_user_id(user_id)
        if not user_session:
            return False

        await self.db.delete(user_session)
        await self.db.commit()
        return True
    


    async def update_user_session_by_dict(self, user_id: int, update_data: dict):
        user_session = await self.get_active_user_session_by_user_id(user_id)
        if not user_session:
            return None

        # Filter out keys that don't exist on the model
        valid_data = {k: v for k, v in update_data.items() if hasattr(UserSessionModel, k)}
        
        if valid_data:
            stmt = (
                update(UserSessionModel)
                .where(UserSessionModel.id == user_session.id)
                .values(**valid_data)
            )
            await self.db.execute(stmt)
            await self.db.commit()
            await self.db.refresh(user_session)
            
        return user_session