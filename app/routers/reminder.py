from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repository import reminders
from app.schemas.reminders import Reminder, UpdateReminder

router = APIRouter(
    prefix="/reminder",
    tags=["Recordatorios"]
)

@router.get("/")
def get_all_reminders(user_id: int, db : Session = Depends(get_db)): 
    data = reminders.obtener_recordatorios(db,user_id)
    return  data

@router.get("/{reminder_id}")
def get_reminder(reminder_id:int, db : Session = Depends(get_db)):
    data = reminders.obtener_recordatorio(db,reminder_id)
    return data

@router.delete("/")
def delete_reminder(reminder_id: int,  db : Session = Depends(get_db)):
    reminders.eliminar_recordatorio(db, reminder_id)
    return {"status": True, "response": "Recordatorio eliminado correctamente"}

@router.post("/")
def new_reminder(data: Reminder, db : Session = Depends(get_db)):
    r = reminders.crear_recordatorio(db, data)
    return r

@router.patch("/{reminder_id}")
def update_recordatorio(reminder_id:int, data: UpdateReminder, db : Session = Depends(get_db)):
    r= reminders.actualizar_recordatorio(db,data, reminder_id)
    return {"status": True, "response": r}

