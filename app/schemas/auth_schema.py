from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {"email": "john@test.com", "password": "123456"}
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
