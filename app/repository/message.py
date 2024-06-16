from sqlalchemy.orm import Session
from app.db import models
from app.schemas.message import MessageVet, UpdateMessageVet
from fastapi import HTTPException
from sqlalchemy import exc


def crear_mensaje(db: Session, msg: MessageVet):
    temp = msg.dict()
    data = models.MessageVet(
        message_body = temp["message_body"],
        message_title = temp["message_title"],
        pet_id = temp["pet_id"],
        vet_id = temp["vet_id"],
        center_id = temp["center_id"]
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg} 
    db.refresh(data)  
    return data

def obtener_mensaje (db:Session, id: int):
    data = db.query(models.MessageVet).filter(models.MessageVet.message_id == id).first()
    if not data:
        return {"status": False, "response": "Mensaje no encontrado"}                                           
    return data

def obtener_mensajes(db:Session, pet_id:int):
    data = db.query(models.MessageVet).filter(models.MessageVet.pet_id == pet_id).all()
    if not data:
        return                                            
    return data

def eliminar_mensaje (db:Session, id: int):
    data = db.query(models.MessageVet).filter(models.MessageVet.message_id == id)
    if not data.first():
        return {"status": False, "response": "Mensaje no encontrado. No se ha eliminado nada"}                                            
    data.delete(synchronize_session=False)
    db.commit()

def actualizar_mensaje(db: Session, msg: UpdateMessageVet, id: int):
    qry = db.query(models.MessageVet).filter(models.MessageVet.message_id == id)    
    if not qry.first():
         return {"status": False, "response":"Mensaje no encontrado. No se ha podido actualizar."} 
    
    itemqry = qry.first()
    item = msg.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    return itemqry
   
