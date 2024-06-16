from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import vet
from app.schemas.vet import Vet, UpdateVet

router = APIRouter(
    prefix="/vet",
    tags=["Veterinarios"]
)

@router.get("/")
def get_all_veterinarians(db : Session = Depends(get_db)):   # objeto de tipo session que depende de la bbdd
    data = vet.obtener_veterinarios(db)
    return data

@router.get("/{vet_id}")
def get_vet(vet_id:int, db : Session = Depends(get_db)):
    data = vet.obtener_veterinario(db, vet_id)
    return data
  
@router.post("/")
def new_vet(data: Vet, db : Session = Depends(get_db)):
    r = vet.crear_veterinario(db, data)
    return {"status": True, "response": r}

@router.delete("/")
def delete_vet(vet_id: int, db : Session = Depends(get_db)):
    vet.eliminar_veterinario(db, vet_id)
    return {"status": True, "response": "Veterinario eliminado correctamente"}

@router.patch("/{vet_id}")
def update_vet(vet_id: int, data: UpdateVet, db : Session = Depends(get_db)):
    r= vet.actualizar_veterinarios(db,data, vet_id )
    return {"status": True, "response": r}

@router.post("/login")
def login (vet_email: str, vet_pass: str, db:Session= Depends(get_db)):
    r= vet.login(db, vet_email, vet_pass)
    return r