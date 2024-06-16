from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repository import activities
from app.schemas.activities import Activities, UpdateActivities

router = APIRouter(
    prefix="/activities",
    tags=["Actividades"]
)

@router.get("/")
def get_all_activities(pet_id: int, db : Session = Depends(get_db)): 
    data = activities.obtener_actividades(db,pet_id)
    return data

@router.get("/{activity_id}")
def get_activity(activity_id:int, db : Session = Depends(get_db)):
    data = activities.obtener_actividad(db,activity_id)
    return data

@router.delete("/")
def delete_activity(activity_id: int,  db : Session = Depends(get_db)):
    activities.eliminar_actividades(db, activity_id)
    return {"status": True, "response": "Actividad eliminada correctamente"}

@router.post("/")
def new_activity(data: Activities, db : Session = Depends(get_db)):
    r = activities.crear_actividad(db, data)
    return {"status": True, "response": r}

@router.patch("/{activity_id}")
def update_activity(activity_id:int, data: UpdateActivities, db : Session = Depends(get_db)):
    r= activities.actualizar_actividades(db,data, activity_id)
    return {"status": True, "response": r}

