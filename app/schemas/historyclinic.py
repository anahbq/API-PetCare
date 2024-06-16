from pydantic import BaseModel 
from typing import Optional
from datetime import datetime

class ClinicHistory(BaseModel):
    motive :str 
    illness : str | None= ""
    medical_examination : str | None= ""
    diagnostic : str | None= ""
    prognosis : str| None= ""
    treatment : str| None= ""
    coments :str| None= ""
    vet_id : int
    pet_id : int

class ViewClinicHistory(ClinicHistory):
    history_id : int
    creation :datetime
    modify : datetime
    class Config():
        orm_mode = True


class UpdateClinicHistory(BaseModel):
    motive :str = None
    illness : str = None
    medical_examination : str = None
    diagnostic : str = None
    prognosis : str= None
    treatment : str= None
    coments :str= None
    
   
   
