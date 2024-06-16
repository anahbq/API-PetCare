from pydantic import BaseModel  
from typing import Optional
from datetime import datetime
  
class Activities(BaseModel):
    activity_name : str
    activity_type : str
    activity_time_start: datetime
    activity_time_end: datetime | None = None
    activity_comments: str
    activity_minutes: str
    pet_id : int

class ViewActivities(Activities):
    activity_id: int    
    creation : datetime
    modify: datetime
 
    class Config():
        orm_mode = True

class UpdateActivities(BaseModel):
    activity_name : str= None
    activity_type : str= None
    activity_time_start: datetime = None
    activity_time_end: datetime= None
    activity_minutes: str = None
    activity_comments: str= None

