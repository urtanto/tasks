from pydantic import UUID4, BaseModel, EmailStr, Field

from src.schemas.response import BaseCreateResponse, BaseResponse


class UserID(BaseModel):
    id: UUID4


class CreateUserRequest(BaseModel):
    full_name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=120)


class UserDB(UserID, CreateUserRequest):
    pass


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UserResponse(BaseResponse):
    payload: UserDB
