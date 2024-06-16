from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import user
from app.schemas.user import User, UpdateUser

router = APIRouter(
    prefix="/user",
    tags=["Usuarios"]
)

@router.get("/")
def get_all_user(db : Session = Depends(get_db)):   # objeto de tipo session que depende de la bbdd
    data = user.obtener_usuarios(db)
    return {"status": True, "response": data}

@router.get("/{user_id}")
def get_user(user_id:int, db : Session = Depends(get_db)):
    data = user.obtener_usuario(db, user_id)
    return data
  
@router.post("/")
def new_user(data: User, db : Session = Depends(get_db)):
    r = user.crear_usuario(db, data)
    return {"status": True, "response": r}

@router.delete("/")
def delete_user(user_id: int, db : Session = Depends(get_db)):
    user.eliminar_usuario(db, user_id)
    return {"status": True, "response": "Usuario eliminado correctamente"}

@router.patch("/{user_id}")
def update_user(user_id: int, data: UpdateUser, db : Session = Depends(get_db)):
    r= user.actualizar_usuario(db,data, user_id )
    return r

@router.post("/login")
def login (user_email: str, user_pass: str, db:Session= Depends(get_db)):
    r= user.login(db, user_email, user_pass)
    return r