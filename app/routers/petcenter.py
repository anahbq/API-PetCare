from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import petcenter
from app.schemas.petcenter import PetCenter, UpdatePetCenter

router = APIRouter(
    prefix="/center",
    tags=["Centro veterinario"]
)

@router.get("/")
def get_all_centers(db : Session = Depends(get_db)): 
    data = petcenter.obtener_centros(db)
    return data

@router.get("/{center_id}")
def get_center(center_id:int, db : Session = Depends(get_db)):
    data = petcenter.obtener_centro(db,center_id)
    return data
  
@router.post("/")
def new_center(data: PetCenter, db : Session = Depends(get_db)):
    r = petcenter.crear_centro(db, data)
    return {"status": True, "response": r}

@router.delete("/")
def delete_center(center_id: int,db : Session = Depends(get_db)):
    petcenter.eliminar_centro(db, center_id)
    return {"status": True, "response": "Centro eliminado correctamente"}

@router.patch("/{center_id}")
def update_center(center_id:int, data: UpdatePetCenter, db : Session = Depends(get_db)):
    r= petcenter.actualizar_centro(db,data,center_id)
    return r

@router.patch("/val/{center_id}")
def valoration (center_id: int, votes: int, db:Session = Depends(get_db)):
    r = petcenter.valoration(db,center_id, votes)
    return {"status": True}

