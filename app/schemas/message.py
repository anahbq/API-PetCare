from pydantic import BaseModel  ##nos permite describir los datos para usarlos luego
from typing import Optional
from datetime import datetime

class MessageVet(BaseModel):
    message_body: str
    message_title : str
    pet_id : int
    vet_id : int |  None = None
    center_id: int
   

class ViewMessageVet(MessageVet):
    message_id : int
    message_response: str
    creation: datetime
    modify : datetime  
    class Config():
        orm_mode = True

class UpdateMessageVet(BaseModel):
    vet_id : int = None
    center_id: int = None
    message_response: str = None
   
    
    