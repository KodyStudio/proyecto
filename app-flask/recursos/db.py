# heroku account - correo: justinsilvac360@gmail.com password: KE:Y3fjpp.3MTb_ nombre:inventorycontrol
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

# Carga las variables de entorno que tengo en .env
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
db.execute("CREATE TABLE users(id SERIAL PRIMARY KEY NOT NULL, username VARCHAR NOT NULL, hash VARCHAR NOT NULL)")
db.commit()
print("tablas creadas")
