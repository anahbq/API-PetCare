from sqlalchemy.orm import Session
from app.db import models
from app.schemas.activities import Activities, UpdateActivities
from fastapi import HTTPException
from sqlalchemy import exc


def crear_actividad(db: Session, info: Activities):
    temp = info.dict()
    data = models.Activities(
        activity_name = temp["activity_name"],
        activity_type  = temp["activity_type"],
        activity_time_start = temp["activity_time_start"],
        activity_time_end = temp["activity_time_end"],
        activity_comments = temp["activity_comments"],
        activity_minutes = temp["activity_minutes"],
        pet_id  = temp["pet_id"]
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    db.refresh(data)  
    return data

def obtener_actividad (db:Session, id: int):
    data = db.query(models.Activities).filter(models.Activities.activity_id == id).first()
    if not data:
        return {"status": False, "response": "Actividad no encontrada."}                                            
    return data

def obtener_actividades(db:Session, pet_id:int):
    data = db.query(models.Activities).filter(models.Activities.pet_id == pet_id).all()
    if not data:
        return {"status": False, "response": "Actividades no encontradas."}                                            
    return data

def eliminar_actividades (db:Session, id: int):
    data = db.query(models.Activities).filter(models.Activities.activity_id == id)
    if not data.first():
        return {"status": False, "response": "Actividad no encontrada. No se ha eliminado nada"}                                              
    data.delete(synchronize_session=False)
    db.commit()

def actualizar_actividades(db: Session, info: UpdateActivities, id: int):
    qry = db.query(models.Activities).filter(models.Activities.activity_id == id)    
    if not qry.first():
         return {"status": False, "response":"Actividad no encontrada. No se ha podido actualizar."}
    
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
   
