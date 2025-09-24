from sqlmodel import SQLModel ,Field,func,Column,DateTime
import uuid
from datetime import datetime,date
import sqlalchemy.dialects.postgresql as pg

class User (SQLModel,table =True):
    __tablename__='users'

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    first_name: str
    last_name: str
    email: str = Field(unique=True, nullable=False, max_length=40, index=True)
    password: str = Field(exclude=True)
    is_verified: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )