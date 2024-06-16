from pydantic import BaseModel  
from typing import Optional
from datetime import datetime

from app.schemas.pets import ViewPet


class User(BaseModel):
    user_name: str
    user_lastname: str
    user_email: str
    user_pass: str
    user_birthdate: datetime

class UserView(User):
    user_id: int
    creation: datetime
    user_state: bool
    modify: datetime
    class Config():
        orm_mode = True

class UpdateUser(BaseModel):
    user_name: str = None
    user_lastname: str = None
    user_email: str = None
    user_pass: str = None
    user_birthdate: datetime= None
    user_state: bool= None
