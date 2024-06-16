from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import pets
from app.schemas.pets import Pet, UpdatePet

router = APIRouter(
    prefix="/pet",
    tags=["Mascotas"]
)

@router.get("/")
def get_all_pets(user_id: int, db : Session = Depends(get_db)): 
    data = pets.obtener_mascotas(db, user_id)
    return data

@router.get("/{pet_id}")
def get_pet(pet_id:int, db : Session = Depends(get_db)):
    data = pets.obtener_mascota(db, pet_id)
    return data
@router.get("/vet/{vet_id}")
def get_pets_center(vet_id:int, db : Session = Depends(get_db)):
    data = pets.obtener_mascotas_center(db, vet_id)
    return data
  
@router.post("/")
def new_pet(data: Pet, db : Session = Depends(get_db)):
    r = pets.crear_mascota(db, data)
    return {"status": True, "response": r}

@router.delete("/")
def delete_pet(user_id: int, pet_id:int, db : Session = Depends(get_db)):
    pets.eliminar_mascota(db, pet_id, user_id)
    return {"status": True, "response": "Mascota eliminado correctamente"}

@router.patch("/{pet_id}")
def update_pet(pet_id:int, data: UpdatePet, db : Session = Depends(get_db)):
    r= pets.actualizar_mascota(db,data, pet_id)
    return {"status": True, "response": r}

@router.patch("/id/{pet_id}")
def update_center(pet_id:int, center_id: int, db : Session = Depends(get_db)):
    r= pets.actualizar_center(db,center_id, pet_id)
    return {"status": True, "response": r}
