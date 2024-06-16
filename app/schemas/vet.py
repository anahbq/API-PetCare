from pydantic import BaseModel  ##nos permite describir los datos para usarlos luego
from typing import Optional
from datetime import datetime

class Vet(BaseModel):
    vet_name : str
    vet_email : str
    vet_pass : str
    vet_dni : str
    vet_photo : str | None = ""
    vet_information: str | None=""
    center_id : int | None = None

   

class ViewVet(Vet):
    vet_id :int 
    creation : datetime
    modify : datetime
    vet_status : bool
    class Config():
        orm_mode = True

class UpdateVet(BaseModel):
    vet_name : str= None
    vet_email : str= None
    vet_pass : str= None
    vet_dni : str= None
    vet_photo : str = None
    vet_information: str = None
    vet_status : bool= None
    center_id : int= None

    
