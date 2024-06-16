from pydantic import BaseModel 
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    post_title : str 
    post_body:str
    post_category : str
    post_type_animal : str
    vet_id : int
    post_img: str | None = ""
    post_author: str
   

class ViewPost(Post):
    post_id : int
    creation: datetime
    modify : datetime
    valoration: int
    class Config():
        orm_mode = True

class UpdatePost(BaseModel):
    post_title : str = None
    post_img: str = None
    post_body:str= None
    post_category : str= None
    post_type_animal : str= None
    vet_id : int= None
    valoration: int = None
    post_author: str = None

    
   