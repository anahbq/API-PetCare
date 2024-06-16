#consultas a bbdd
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.petcenter import PetCenter, UpdatePetCenter
from fastapi import HTTPException
from sqlalchemy import exc


def crear_centro(db: Session, center: PetCenter):
    temp = center.dict()
    data = models.PetCenter(
        center_name = temp["center_name"],
        center_street  = temp["center_street"],
        center_information  = temp["center_information"],
        center_logo  = temp["center_logo"],
        email_admin = temp["email_admin"],
        center_nif = temp["center_nif"],
        center_phone = temp["center_phone"]
        )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    db.refresh(data)  
    return data

def obtener_centro (db:Session, center_id: int):
    data = db.query(models.PetCenter).filter(models.PetCenter.center_id == center_id).first()
    if not data:
        raise HTTPException (status_code = 404, detail={"status": False, "response": "Centro no encontrado"})                                              
    return data

def obtener_centros (db:Session):
    data = db.query(models.PetCenter).all()
    if not data:
        raise HTTPException (status_code = 404, detail={"status": False, "response": "Centros no encontrados"})                                              
    return data

def eliminar_centro (db:Session, center_id: int):
    data = db.query(models.PetCenter).filter(models.PetCenter.center_id == center_id)
    if not data.first():
        raise HTTPException (status_code = 404, detail={"status": False, "response": "Centro no encontrado. No se ha eliminado nada"})                                              
    data.delete(synchronize_session=False)
    db.commit()

def actualizar_centro(db: Session, center: UpdatePetCenter, center_id:int):
    qry = db.query(models.PetCenter).filter(models.PetCenter.center_id == center_id)    
    if not qry.first():
         return {"status": False, "response":"Centro no encontrado. No se ha podido actualizar."} 
    
    itemqry = qry.first()
    item = center.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    return {"status": True, "response": itemqry}
   
def valoration (db:Session, center_id: int, votes: int):
    data = db.query(models.PetCenter).filter(models.PetCenter.center_id == center_id).first()
    if not data:
        return {"status": False, "response": "Centro no encontrado"} 
    if data.center_valoration is None:
        data.center_valoration = 0
    data.center_valoration += votes                                    
    db.commit()
    db.refresh(data)

