from pydantic import BaseModel, ConfigDict, Field


class AdminSchema(BaseModel):
    username: str = Field(..., description="user名")

class LoginAdmin(AdminSchema):
    password: str = Field(..., description="パスワード")


class GenerateAdmin(LoginAdmin):
    token: str = Field(..., description="トークン", exclude=True)

    model_config = ConfigDict(from_attributes=True)

class AdminOut(AdminSchema):
    id: int = Field(..., description="id")
    username: str = Field(..., description="user名")

class Token(BaseModel):
    access_token: str
    token_type: str
