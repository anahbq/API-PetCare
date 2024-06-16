from fastapi import FastAPI
from app.routers import user, vet, pets,post,reminder,petcenter,message,clinichistory,activities
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:62125",
    "http://localhost",
    "http://localhost:4200",
]

def create_table():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


create_table()


app.include_router(user.router)
app.include_router(vet.router)
app.include_router(pets.router)
app.include_router(reminder.router)
app.include_router(post.router)
app.include_router(petcenter.router)
app.include_router(message.router)
app.include_router(clinichistory.router)
app.include_router(activities.router)





