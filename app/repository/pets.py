#consultas a bbdd
from sqlalchemy.orm import Session
from app.schemas.pets import Pet, UpdatePet
from fastapi import HTTPException
from sqlalchemy import exc
from app.db import models


def crear_mascota(db: Session, pet: Pet):
    temp = pet.dict()
    data = models.Pets(
        user_id = temp["user_id"],
        pet_name= temp["pet_name"],  
        pet_chip = temp["pet_chip"], 
        pet_specie = temp["pet_specie"],
        pet_race= temp["pet_race"],
        pet_sex= temp["pet_sex"],
        pet_birthdate = temp["pet_birthdate"],
        pet_siteimplantation = temp["pet_siteimplantation"],
        pet_dateimplantation = temp["pet_dateimplantation"],
        pet_color = temp["pet_color"], 
        pet_characteristics= temp["pet_characteristics"],
        center_id = temp["center_id"]
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException (status_code = 400, detail={"status": False, "response":err_msg}) 
    db.refresh(data)  
    return data

def obtener_mascota (db:Session, pet_id: int):
    data = db.query(models.Pets).filter(models.Pets.pet_id == pet_id).first()
    if not data:
        raise HTTPException (status_code = 404, detail={"status": False, "response": f"Mascota no encontrada para el usuario {user_id}."})                                              
    return data

def eliminar_mascota (db:Session, pet_id: int, user_id: int):
    data = db.query(models.Pets).filter(models.Pets.pet_id == pet_id, models.Pets.user_id == user_id)
    if not data.first():
        raise HTTPException (status_code = 404, detail={"status": False, "response": "Mascota no encontrada."})                                              
    data.delete(synchronize_session=False)
    db.commit()

def obtener_mascotas(db: Session, user_id: int):
    data = db.query(models.Pets).filter(models.Pets.user_id == user_id).all()
    if not data:
        return {"status": False, "response": "No hay datos de mascotas"}                                             
    return data

def obtener_mascotas_center(db: Session, vet_id: int):
    data = db.query(models.Vet).filter(models.Vet.vet_id == vet_id).first()
    if not data:
        return {"status": False, "response": "No hay veterinario"}     
    data2 = db.query(models.Pets).filter(models.Pets.center_id == data.center_id).all()
    if not data2:
        return {"status": False, "response": "No hay datos de mascotas"}     
    return data2

def actualizar_mascota(db: Session, pet: UpdatePet, pet_id:int):
    qry = db.query(models.Pets).filter( models.Pets.pet_id == pet_id)    
    if not qry.first():
         raise HTTPException (status_code = 404, detail={"status": False, "response":"Mascota no encontrada. No se ha podido actualizar."}) 
    
    itemqry = qry.first()
    item = pet.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException (status_code = 400, detail={"status": False, "response":err_msg}) 
    return itemqry


def actualizar_center(db: Session,center_id: int , pet_id:int):
    qry = db.query(models.Pets).filter( models.Pets.pet_id == pet_id)    
    if not qry.first():
         return {"status": False, "response":"Mascota no encontrada. No se ha podido actualizar."} 
    
    itemqry = qry.first()
    itemqry.center_id = center_id
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    return itemqry
   
