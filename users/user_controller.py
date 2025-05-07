from sqlalchemy.orm import Session
import bcrypt
import users.user_model as models
from sqlalchemy import text

async def create_user(db: Session, user_data: models.User):
    new_id = db.execute(text("SELECT uuid_generate_v4()")).scalar()

    hashed_pw = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    user_data.password = hashed_pw.decode('utf-8')
    db_registro = models.User(**user_data.model_dump())
    db_registro.id = new_id

    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    
    return db_registro

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
