#consultas a bbdd
import uuid
from sqlalchemy.orm import Session
from app.schemas.vet import Vet, UpdateVet
from fastapi import HTTPException
from sqlalchemy import exc
from app.db import models


def crear_veterinario(db: Session, vet: Vet):
    temp = vet.dict()
    data = models.Vet(
        vet_name = temp["vet_name"],
        vet_email  = temp["vet_email"],
        vet_pass  = temp["vet_pass"],
        vet_dni  = temp["vet_dni"],
        vet_photo  = temp["vet_photo"],
        vet_information = temp["vet_information"],
        center_id  = temp["center_id"]
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException (status_code = 400, detail={"status": False, "response":err_msg}) 
    db.refresh(data)  
    return data.vet_id

def obtener_veterinario (db:Session, vet_id: int):
    data = db.query(models.Vet).filter(models.Vet.vet_id == vet_id).first()
    if not data:
        raise HTTPException (status_code = 404, detail={"status": False, "response": "Veterinario no encontrado"})                                              
    return data

def eliminar_veterinario (db:Session, vet_id: int):
    data = db.query(models.Vet).filter(models.Vet.vet_id == vet_id)
    if not data.first():
        raise HTTPException (status_code = 404, detail={"status": False, "response": "Veterinario no encontrada."})                                              
    data.delete(synchronize_session=False)
    db.commit()

def obtener_veterinarios(db: Session):
    data = db.query(models.Vet).all()
    if not data:
        raise HTTPException (status_code = 404, detail={"status": False, "response": "No hay datos de veterinarios."})                                              
    return data

def actualizar_veterinarios(db: Session, vet: UpdateVet, vet_id:int):
    qry = db.query(models.Vet).filter(models.Vet.vet_id == vet_id)    
    if not qry.first():
         raise HTTPException (status_code = 404, detail={"status": False, "response":"Veterinario no encontrada. No se ha podido actualizar."}) 
    
    itemqry = qry.first()
    item = vet.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException (status_code = 400, detail={"status": False, "response":err_msg}) 
    return itemqry

def login (db:Session, vet_email: str, vet_pass: str):
    data = db.query(models.Vet).filter(models.Vet.vet_email == vet_email, models.Vet.vet_pass == vet_pass).first()
    if not data:
        return {"status": False, "response": "Usuario incorrecto. Revise email o contraseña."}
    if(data.vet_status == False):
        return {"status": False, "response": "Usuario deshabilitado."}

    
    return {"status": True, "response": "Bienvenido", "token": uuid.uuid4(), "id": data.vet_id}


