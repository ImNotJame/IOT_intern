from sqlalchemy import Integer, Column, String

from database.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column("u_id",Integer, primary_key=True, index=True)
    username = Column("u_username",String, nullable=False)
    hashed_password = Column("u_password",String, nullable=False)