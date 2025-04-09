from sqlalchemy.orm import Session
import bcrypt
import models.user_model as models

def create_user(db: Session, user_data: models.User):
    hashed_pw = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    user_data.password = hashed_pw
    db_registro = models.User(**user_data.model_dump())
    db.add(db_registro)
    db.commit()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
