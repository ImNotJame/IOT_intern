from sqlalchemy import String, Integer, Column, ForeignKey, BOOLEAN, DateTime

from database.database import Base


class UserSessionModel(Base):
    __tablename__ = "user_sessions"
    id = Column("us_id", Integer, primary_key=True, index=True)
    user_id = Column("u_id", Integer, ForeignKey("users.u_id"), index=True, nullable=False)
    user_jwt_token = Column("us_jwt_token",String(255), nullable=False)
    user_refresh_token = Column("us_refresh_token",String(255), nullable=False)
    user_login_time = Column("us_login_time", DateTime(timezone=True), nullable=False)
    user_logout_time = Column("us_logout_time", DateTime(timezone=True), nullable=True)
    user_flag = Column("us_flag", BOOLEAN, nullable=False)
