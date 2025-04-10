from connection import engine
from models.user_model import User

print("Creando tablas en la base de datos...")
User.Base.metadata.create_all(bind=engine)
print("¡Listo! 🛠️")