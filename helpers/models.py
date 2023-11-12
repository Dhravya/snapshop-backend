from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    email: str
    image: str
    gender: str

class TryOnImage(BaseModel):
    original_image: str
    user_email: str