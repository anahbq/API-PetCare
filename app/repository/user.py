#consultas a bbdd
from sqlalchemy.orm import Session
from app.db import models
from typing import List
from app.schemas.user import User, UserView, UpdateUser
from fastapi import HTTPException
from sqlalchemy import exc
import uuid


def crear_usuario(db: Session, user: User):
    temp = user.dict()
    data = models.User(
        user_name= temp["user_name"],
        user_lastname= temp["user_lastname"],
        user_email= temp["user_email"],
        user_pass= temp["user_pass"],
        user_birthdate= temp["user_birthdate"],
        user_state= True,
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg} 
    db.refresh(data)  
    return "Bienvenido a PetCare. Has creado tu cuenta correctamente."

def obtener_usuario (db:Session, user_id: int):
    data = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not data:
        return {"status": False, "response": "Usuario no encontrado."}                                           
    return data

def eliminar_usuario (db:Session, user_id: int):
    data = db.query(models.User).filter(models.User.user_id == user_id)
    if not data.first():
        return {"status": False, "response": "Usuario no encontrado."}                                             
    data.delete(synchronize_session=False)
    db.commit()

def obtener_usuarios(db: Session):
    data = db.query(models.User).all()
    return data

def actualizar_usuario(db: Session, user: UpdateUser, user_id:int):
    qry = db.query(models.User).filter(models.User.user_id == user_id)    
    if not qry.first():
         return {"status": False, "response":"Usuario no encontrado. No se ha podido actualizar."}
    
    itemqry = qry.first()
    item = user.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg} 
    return {"status": True, "response":"Actualizado"}

def login (db:Session, user_email: str, user_pass: str):
    data = db.query(models.User).filter(models.User.user_email == user_email, models.User.user_pass == user_pass).first()
    if not data:
        return {"status": False, "response": "Usuario incorrecto. Revise email o contraseña."}
    return {"status": True, "response": "Bienvenido", "token": uuid.uuid4(), "id": data.user_id}

