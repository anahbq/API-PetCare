from app.db.database import Base
from sqlalchemy import Column,Integer,String, Boolean, DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class PetCenter(Base):
    __tablename__= "petCenter"
    center_id = Column(Integer, primary_key=True, autoincrement= True)
    center_name = Column(String)
    center_street = Column(String)
    center_valoration = Column(Integer)
    center_information = Column(String)
    center_logo = Column(String)
    creation =  Column(DateTime,  default= datetime.now)
    email_admin = Column(String)
    modify = Column(DateTime,  default= datetime.now, onupdate=datetime.now)
    vets = relationship("Vet", backref="Vet")
    pets = relationship("Pets", backref="Pets")
    message = relationship("MessageVet", backref="MessageVet")
    center_nif=  Column(String)
    center_phone  = Column(String)

class Vet(Base):
    __tablename__ = "veterinarians"
    vet_id = Column(Integer, primary_key=True, autoincrement= True)
    vet_name = Column(String)
    vet_email = Column(String, unique= True)
    vet_pass = Column(String)
    vet_dni = Column(String, unique= True)
    vet_photo = Column(String)
    vet_status = Column(Boolean, default=False)
    vet_information = Column (String(1024))
    creation = Column(DateTime,  default= datetime.now)
    modify = Column(DateTime,  default= datetime.now, onupdate=datetime.now)
    center_id = Column(Integer, ForeignKey(PetCenter.center_id))
    posts =  relationship("Post", backref="Post", cascade ="merge")
    

class User(Base):
    __tablename__ = "user"
    user_id =  Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    user_lastname = Column(String)
    user_email = Column(String, unique=True)
    user_pass = Column(String)
    user_birthdate = Column(DateTime)
    creation = Column(DateTime, default= datetime.now)
    user_state = Column(Boolean, default=False)
    pets = relationship("Pets", backref="User", cascade="delete, merge")
    modify = Column(DateTime,  default= datetime.now, onupdate=datetime.now)
    reminders = relationship("Reminders", backref= "Reminders", cascade="delete, merge")

class Pets(Base):
    __tablename__ = "pets"
    pet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id,  ondelete="CASCADE"))
    pet_name= Column(String)
    pet_img = Column (String)
    pet_chip = Column(String)
    pet_specie = Column(String)
    pet_race = Column(String)
    pet_sex = Column(String)
    pet_birthdate = Column(DateTime)
    pet_siteimplantation = Column(String)
    pet_dateimplantation = Column(DateTime)
    pet_color = Column(String)
    pet_characteristics = Column(String(1024))
    center_id = Column(Integer, ForeignKey(PetCenter.center_id))
    activities = relationship("Activities", backref="Activities", cascade="delete, merge")
    clinic_history = relationship("ClinicHistory", backref="ClinicHistory")
    creation = Column(DateTime,  default= datetime.now)
    modify = Column(DateTime,  default= datetime.now, onupdate=datetime.now)


class ClinicHistory(Base):
    __tablename__ = "ClinicHistory"
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    motive = Column (String)
    illness = Column (String)
    medical_examination = Column (String(2048))
    diagnostic = Column (String(2048))
    prognosis = Column (String(2048))
    treatment = Column (String(2048))
    coments = Column (String(2048))
    creation = Column(DateTime,  default= datetime.now)
    modify = Column(DateTime, default= datetime.now, onupdate=datetime.now)
    vet_id = Column(Integer, ForeignKey(Vet.vet_id))
    pet_id = Column(Integer, ForeignKey(Pets.pet_id))



class Post(Base):
    __tablename__ = "Posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    post_title = Column (String)
    post_body = Column (String)
    post_category = Column (String)
    post_img = Column(String)
    post_type_animal = Column(String)
    post_author = Column(String)
    vet_id = Column(Integer, ForeignKey(Vet.vet_id))
    valoration = Column(Integer, default=0)
    creation = Column(DateTime,  default= datetime.now)
    modify = Column(DateTime,  default= datetime.now, onupdate=datetime.now)

class MessageVet(Base):
    __tablename__ = "Communication Center Vet"
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    message_body = Column(String(1024))
    message_title = Column(String(250))
    message_response = Column(String(1024))
    pet_id = Column(Integer, ForeignKey(Pets.pet_id))
    vet_id = Column(Integer, ForeignKey(Vet.vet_id))
    center_id = Column(Integer, ForeignKey(PetCenter.center_id))
    creation = Column(DateTime,  default= datetime.now)
    modify = Column(DateTime, default= datetime.now, onupdate=datetime.now)

class Activities(Base):
    __tablename__ = "Activities"
    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    activity_name = Column(String)
    activity_type = Column(String)
    activity_time_start = Column (DateTime)
    activity_time_end = Column (DateTime)
    activity_minutes = Column(String)
    activity_comments = Column(String)
    pet_id = Column(Integer, ForeignKey(Pets.pet_id))
    creation = Column(DateTime,  default= datetime.now)
    modify = Column(DateTime, default= datetime.now, onupdate=datetime.now)

class Reminders(Base):
    __tablename__ = "Reminders"
    reminder_id = Column(Integer, primary_key=True, autoincrement=True)
    reminder_title = Column(String)
    reminder_date = Column(String)
    reminder_comments = Column (String)
    reminder_status = Column (Boolean, default= True)
    user_id = Column(Integer, ForeignKey(User.user_id))

    creation = Column(DateTime,  default= datetime.now)
    modify = Column(DateTime, default= datetime.now, onupdate=datetime.now)
