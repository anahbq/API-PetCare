from sqlalchemy.orm import Session
from app.db import models
from app.schemas.post import Post, UpdatePost
from fastapi import HTTPException
from sqlalchemy import exc


def crear_post(db: Session, Post: Post):
    temp = Post.dict()
    data = models.Post(
        post_title = temp["post_title"],
        post_body = temp["post_body"],
        post_category = temp["post_category"],
        post_type_animal = temp["post_type_animal"],
        vet_id= temp["vet_id"],
        post_author = temp["post_author"],
        post_img = temp["post_img"]
    )
    try:
        db.add(data)           
        db.commit()
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    db.refresh(data)  
    return data

def obtener_post (db:Session, Post_id: int):
    data = db.query(models.Post).filter(models.Post.post_id == Post_id).first()
    if not data:
        return {"status": False, "response": "Post no encontrado."}                                             
    return data

def obtener_mis_post (db:Session, vet_id: int):
    data = db.query(models.Post).filter(models.Post.vet_id == vet_id).all()
    if not data:
        return {"status": False, "response": "Posts no encontrado."}                                            
    return data


def eliminar_post (db:Session, Post_id: int):
    data = db.query(models.Post).filter(models.Post.post_id == Post_id)
    if not data.first():
        return {"status": False, "response": "Post no encontrado."}                                             
    data.delete(synchronize_session=False)
    db.commit()

def obtener_posts(db: Session):
    data = db.query(models.Post).all()
    return data

def actualizar_post(db: Session, Post: UpdatePost, Post_id:int):
    qry = db.query(models.Post).filter(models.Post.post_id == Post_id)    
    if not qry.first():
         return {"status": False, "response":"Post no encontrado. No se ha podido actualizar."}
    
    itemqry = qry.first()
    item = Post.model_dump(exclude_unset=True)

    for key, value in item.items():
        setattr(itemqry, key, value)
    
    try:
        db.commit()
        db.refresh(itemqry)
    except exc.IntegrityError as e:
        err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
        return {"status": False, "response":err_msg}
    return itemqry
   
def valoration (db:Session, post_id: int, votes: int):
    data = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    if not data:
        return {"status": False, "response": "Post no encontrado"} 
    if data.valoration is None:
        data.valoration = 0
    data.valoration += votes                                    
    db.commit()
    db.refresh(data)