#consultas a bbdd
from sqlalchemy.orm import Session
from app.schemas.historyclinic import ClinicHistory, UpdateClinicHistory
from fastapi import HTTPException
from sqlalchemy import exc
from app.db import models


def crear_historia(db: Session, historia: ClinicHistory):
    temp = historia.dict()
    data = models.ClinicHistory(
        motive = temp["motive"],
        illness  = temp["illness"],
        medical_examination  = temp["medical_examination"],
        diagnostic  = temp["diagnostic"],
        prognosis = temp["prognosis"],
        treatment  = temp["treatment"],
        coments  = temp["coments"],
        vet_id  = temp["vet_id"],
        pet_id = temp["pet_id"],
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg} 
    db.refresh(data)  
    return data

def obtener_historia (db:Session, history_id: int):
    data = db.query(models.ClinicHistory).filter(models.ClinicHistory.history_id == history_id).first()
    if not data:
        return {"status": False, "response": "Historia no encontrada"}                                             
    return data

def obtener_historias(db: Session, pet_id:int):
    data = db.query(models.ClinicHistory).filter(models.ClinicHistory.pet_id==pet_id).all()
    if not data:
        return {"status": False, "response": "No hay datos."}                                            
    return data

def actualizar_historia(db: Session, history: UpdateClinicHistory, history_id:int):
    qry = db.query(models.ClinicHistory).filter(models.ClinicHistory.history_id == history_id)    
    if not qry.first():
         return {"status": False, "response":"Historia no encontrada. No se ha podido actualizar."} 
    
    itemqry = qry.first()
    item = history.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    return itemqry
   
def eliminar_historia (db:Session, id: int):
    data = db.query(models.ClinicHistory).filter(models.ClinicHistory.history_id == id)
    if not data.first():
        return {"status": False, "response": "Historia no encontrada. No se ha eliminado nada"}                                              
    data.delete(synchronize_session=False)
    db.commit()
    return {"status": True, "response": "Eliminado."}