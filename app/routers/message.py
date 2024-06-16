from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import message
from app.schemas.message import MessageVet, UpdateMessageVet

router = APIRouter(
    prefix="/message",
    tags=["Mensajes Centro veterinario"]
)

@router.get("/")
def get_all_messages(pet_id: int, db : Session = Depends(get_db)): 
    data = message.obtener_mensajes(db,pet_id)
    return  data

@router.get("/{msg_id}")
def get_message(msg_id:int, db : Session = Depends(get_db)):
    data = message.obtener_mensaje(db,msg_id)
    return data
  
@router.post("/")
def new_message(data: MessageVet, db : Session = Depends(get_db)):
    r = message.crear_mensaje(db, data)
    return {"status": True, "response": r}

@router.delete("/")
def delete_message(msg_id: int,db : Session = Depends(get_db)):
    message.eliminar_mensaje(db, msg_id)
    return {"status": True, "response": "Mensaje eliminado correctamente"}

@router.patch("/{msg_id}")
def update_message(msg_id:int, data: UpdateMessageVet, db : Session = Depends(get_db)):
    r= message.actualizar_mensaje(db,data, msg_id)
    return {"status": True, "response": r}

