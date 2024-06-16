from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import clinichistory
from app.schemas.historyclinic import ClinicHistory, UpdateClinicHistory

router = APIRouter(
    prefix="/history",
    tags=["Historial médico"]
)

@router.get("/")
def get_all_history(pet_id: int, db : Session = Depends(get_db)): 
    data = clinichistory.obtener_historias(db,pet_id)
    return data

@router.get("/{history_id}")
def get_history(history_id:int, db : Session = Depends(get_db)):
    data = clinichistory.obtener_historia(db, history_id)
    return  data
  
@router.post("/")
def new_history(data: ClinicHistory, db : Session = Depends(get_db)):
    r = clinichistory.crear_historia(db, data)
    return {"status": True, "response": r}

@router.patch("/{history_id}")
def update_history(history_id:int, data: UpdateClinicHistory, db : Session = Depends(get_db)):
    r= clinichistory.actualizar_historia(db,data, history_id)
    return {"status": True, "response": r}

@router.delete("/{history_id}")
def delete_history(history_id:int, db : Session = Depends(get_db)):
    r = clinichistory.eliminar_historia(db, history_id)
    return  r
