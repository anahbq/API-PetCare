from pydantic import BaseModel  
from typing import Optional
from datetime import datetime
  
class Reminder(BaseModel):
    reminder_title: str
    reminder_date: str | None = None
    reminder_comments: str | None = ""
    user_id: int

class ViewReminder(Reminder):
    reminder_id: int    
    reminder_status: bool 
    creation : datetime
    modify: datetime
 
    class Config():
        orm_mode = True

class UpdateReminder(BaseModel):
    reminder_title: str  = None
    reminder_date: str = None
    reminder_comments: str  = None
    reminder_status: bool  = None
   
