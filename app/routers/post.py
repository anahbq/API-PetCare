from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repository import post
from app.schemas.post import Post, UpdatePost
from app.db import models

router = APIRouter(
    prefix="/post",
    tags=["Post"]
)

@router.get("/")
def get_all_post(db : Session = Depends(get_db)): 
    data = post.obtener_posts(db)
    return data

@router.get("/{post_id}")
def get_post(post_id:int, db : Session = Depends(get_db)):
    data = post.obtener_post(db, post_id)
    return data

@router.get("/my/{vet_id}")
def get_post(vet_id:int, db : Session = Depends(get_db)):
    data = post.obtener_mis_post(db, vet_id)
    return data
  
@router.post("/")
def new_post(data: Post, db : Session = Depends(get_db)):
    r = post.crear_post(db, data)
    return {"status": True, "response": r}

@router.delete("/")
def delete_post(post_id: int, db : Session = Depends(get_db)):
    post.eliminar_post(db, post_id)
    return {"status": True, "response": "Post eliminado correctamente"}

@router.patch("/{post_id}")
def update_post(post_id: int, data: UpdatePost, db : Session = Depends(get_db)):
    r= post.actualizar_post(db,data, post_id )
    return {"status": True, "response": r}

@router.patch("/val/{post_id}")
def valoration (post_id: int, votes: int, db:Session = Depends(get_db)):
    r = post.valoration(db,post_id, votes)
    return {"status": True}

