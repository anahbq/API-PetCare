from sqlalchemy.orm import Session
from app.db import models
from app.schemas.reminders import Reminder, UpdateReminder
from fastapi import HTTPException
from sqlalchemy import exc


def crear_recordatorio(db: Session, info: Reminder):
    temp = info.dict()
    data = models.Reminders(
        reminder_title = temp["reminder_title"],
        reminder_date= temp["reminder_date"],
        reminder_comments= temp["reminder_comments"],        
        user_id  = temp["user_id"]
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    db.refresh(data)  
    return {"status": True, "response": data}

def obtener_recordatorio (db:Session, id: int):
    data = db.query(models.Reminders).filter(models.Reminders.reminder_id == id).first()
    if not data:
        return {"status": False, "response": "Recordatorio no encontrado."}                                              
    return data

def obtener_recordatorios(db:Session, user_id:int):
    data = db.query(models.Reminders).filter(models.Reminders.user_id == user_id).all()
    if not data:
        return {"status": False, "response": "Recordatorio no encontrados."}                                              
    return data

def eliminar_recordatorio(db:Session, id: int):
    data = db.query(models.Reminders).filter(models.Reminders.reminder_id == id)
    if not data.first():
        return {"status": False, "response": "Recordatorio no encontrado. No se ha eliminado nada"}                                            
    data.delete(synchronize_session=False)
    db.commit()

def actualizar_recordatorio(db: Session, info: UpdateReminder, id: int):
    qry = db.query(models.Reminders).filter(models.Reminders.reminder_id == id)    
    if not qry.first():
         return {"status": False, "response":"Recordatorio no encontrado. No se ha podido actualizar."} 
    
    itemqry = qry.first()
    item = info.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    return itemqry
   
