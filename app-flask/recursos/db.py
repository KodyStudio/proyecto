# heroku account - correo: justinsilvac360@gmail.com password: KE:Y3fjpp.3MTb_ nombre:inventorycontrol
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

# Carga las variables de entorno que tengo en .env
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# db.execute("INSERT INTO categorias(nombre) VALUES ('Frutas y verduras')")

# restart id
# db.execute("TRUNCATE TABLE categorias RESTART IDENTITY;")

# --Creacion de tablas!
# db.execute("create table categorias(id serial primary key NOT NULL, nombre VARCHAR NOT NULL)")
# db.execute("create table productos(id serial primary key NOT NULL, nombre VARCHAR NOT NULL, costo money NOT NULL, precio money NOT NULL, descripcion VARCHAR(10), imagen VARCHAR,id_categoria integer references categorias)")
# db.execute("create table platillos(id serial primary key NOT NULL, nombre VARCHAR NOT NULL, imagen VARCHAR, descripcion VARCHAR (10))")
# db.execute("create table ventas(id serial primary key NOT NULL, fecha date, cliente VARCHAR NOT NULL, total real)")
# db.execute("create table detalle_venta(id serial primary key NOT NULL, cantidad  integer, id_platillo integer references platillos, id_venta integer references ventas)")
# db.execute("create table detalle_producto(id serial primary key NOT NULL, cantidad_productos integer, id_productos integer references productos, id_platillos integer references platillos)")
# db.execute("ALTER TABLE productos ADD cantidad integer")

db.execute("ALTER TABLE ventas ADD cantidad integer")
db.commit()

print("tablas creadas")
