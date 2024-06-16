from pydantic import BaseModel  ##nos permite describir los datos para usarlos luego
from typing import Optional
from datetime import datetime

class PetCenter(BaseModel):
    center_name : str 
    center_street :str | None = ""
    center_information :str | None = ""
    center_logo : str | None = ""
    email_admin: str
    center_phone:str
    center_nif: str

class ViewPetCenter(PetCenter):
    center_id : int
    center_valoration : int
    creation :  datetime
    modify : datetime

    class Config():
        orm_mode = True

class UpdatePetCenter(BaseModel):
    center_phone:str =None
    center_nif: str = None
    center_name : str  = None
    center_street :str = None
    center_information : str = None
    center_logo : str = None
    center_valoration : int = None
    email_admin: str = None
