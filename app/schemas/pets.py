from pydantic import BaseModel 
from typing import Optional
from datetime import datetime

class Pet(BaseModel):
    user_id : int
    pet_name: str  
    pet_chip : str 
    pet_specie :str
    pet_race :str
    pet_sex:str
    pet_birthdate : datetime
    pet_img: str | None = ""
    pet_siteimplantation :str | None = ""
    pet_dateimplantation : datetime | None
    pet_color :str 
    pet_characteristics:str | None = ""
    center_id : int | None = None
    

class ViewPet(Pet):
    pet_id : int
    creation :datetime
    modify : datetime
   
    class Config():
        orm_mode = True

class UpdatePet(BaseModel):
    pet_name: str  = None
    pet_chip : str = None
    pet_specie :str= None
    pet_race :str= None
    pet_img: str = None
    pet_sex:str= None
    pet_birthdate : datetime= None
    pet_siteimplantation :str = None
    pet_dateimplantation : datetime = None
    pet_color :str = None
    pet_characteristics:str = None
    center_id : int = None