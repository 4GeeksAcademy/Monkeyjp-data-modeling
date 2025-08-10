#  ¿Qué es un ORM? ¿Qué hacen? ¿Cuáles hay?
# ORM significa Object-Relational Mapping (Mapeo Objeto-Relacional).

# Es una herramienta que permite que los desarrolladores trabajen con bases de datos relacionales usando objetos de un lenguaje de programación (por ejemplo, clases y objetos en Python).

# Simplifica la interacción con la base de datos sin tener que escribir consultas SQL manualmente.

# Convierte (mapea) tablas y filas en clases y objetos.

# Ejemplos populares:

# SQLAlchemy (Python)

# Django ORM (Python)


# ¿Qué es Flask?
# Flask es un microframework para construir aplicaciones web en Python.
# Es ligero y flexible, porque no te impone estructura estricta, te deja decidir cómo organizar tu app.
# Te ayuda a crear rutas (endpoints) para que tu app responda a peticiones HTTP (GET, POST, etc.).
# No viene con muchas cosas por defecto, pero puedes agregar extensiones para manejar bases de datos, autenticación, formularios, etc.
# En resumen, Flask es la base para crear sitios web o APIs en Python de forma sencilla y rápida.

# ¿Qué es SQLAlchemy?
# SQLAlchemy es una librería de Python para trabajar con bases de datos relacionales.
# Es un ORM (Object-Relational Mapper), lo que significa que te permite manipular datos de la base como si fueran objetos en Python.
# En vez de escribir directamente SQL, puedes usar clases y métodos para crear, leer, actualizar y borrar registros.
# Te ayuda a que tu código sea más legible, mantenible y menos propenso a errores de SQL.
# Además, puede trabajar con muchas bases de datos distintas (PostgreSQL, MySQL, SQLite, etc.) sin cambiar mucho el código.

# ¿Por qué usamos Flask + SQLAlchemy?
# Flask se encarga de la parte web (rutas, respuestas, solicitudes).
# SQLAlchemy se encarga de la parte de bases de datos, permitiéndote trabajar con datos usando Python puro.
# Esto te ahorra escribir SQL directamente y facilita la interacción con la base de datos.
# Además, SQLAlchemy maneja las relaciones entre tablas (como relationship, ForeignKey), haciendo que manejar datos relacionados sea mucho más intuitivo.



# https://docs.sqlalchemy.org/en/20/orm/index.html  DOCUMENTACION 




# ¿Qué es Mapped[] cuando declaramos un modelo?
# En SQLAlchemy moderna, Mapped[] es una forma de indicar el tipo de dato de un atributo que será mapeado a una columna.

# Es parte de la nueva sintaxis que aprovecha anotaciones de tipo de Python para mejor autocompletado y chequeo estático.

# Ejemplo:

# id: Mapped[int] = mapped_column(primary_key=True)
# name: Mapped[str] = mapped_column()
# Aquí decimos que id es un entero y es la clave primaria, name es una cadena.


#  ¿Qué es db.Model.metadata cuando creamos una tabla?
# db.Model.metadata es un objeto interno que SQLAlchemy usa para registrar información sobre las tablas y esquemas que se van creando.

# Cuando creas una tabla auxiliar con Table() (como para relaciones many-to-many), necesitas pasar metadata para que SQLAlchemy la gestione junto con las demás tablas.

# Es necesario para que SQLAlchemy entienda que esta tabla forma parte del mismo esquema y pueda crearla o actualizarla con los demás modelos.

# Ejemplo:

# favorites_table = Table(
#     "favorites",
#     db.Model.metadata,  # metadata compartida con los modelos
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
#     Column("character_id", ForeignKey("characters.id"), primary_key=True)
# )


# relationship:
# Es una forma en el modelo Python de definir una relación entre dos clases (tablas), que permite acceder fácilmente a los objetos relacionados.

# secondary:
# Se usa en relaciones many-to-many para indicar la tabla intermedia que conecta ambas tablas.


# back_populates
# back_populates sincroniza ambas relaciones en los dos modelos.

# Indica que la relación en una clase corresponde a la relación en la otra, creando así un vínculo bidireccional explícito.

# Esto permite que, cuando cambias la relación en un lado (por ejemplo, asignas un padre a un hijo), automáticamente se actualice la relación inversa (el hijo queda en la lista de hijos del padre).



from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column

db = SQLAlchemy()

favorites_table = Table(
    "favorites",
    db.Model.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("character_id", ForeignKey("characters.id"), primary_key=True)
)

# ¿Qué es db.Model.metadata cuando creamos una tabla?
# db.Model.metadata es un objeto interno que SQLAlchemy usa para registrar información sobre las tablas y esquemas que se van creando.
# Cuando creas una tabla auxiliar con Table() (como para relaciones many-to-many), necesitas pasar metadata para que SQLAlchemy la gestione junto con las demás tablas.
# Es necesario para que SQLAlchemy entienda que esta tabla forma parte del mismo esquema y pueda crearla o actualizarla con los demás modelos.



class Character(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    quote: Mapped[str]

    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorites_table,
        back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "favorited_by": [user.id for user in self.favorited_by]
        }

# ¿Qué es Mapped[] cuando declaramos un modelo?
# En SQLAlchemy moderna, Mapped[] es una forma de indicar el tipo de dato de un atributo que será mapeado a una columna.
# Es parte de la nueva sintaxis que aprovecha anotaciones de tipo de Python para mejor autocompletado y chequeo estático.


# relationship:
# Es una forma en el modelo Python de definir una relación entre dos clases (tablas), que permite acceder fácilmente a los objetos relacionados.

# secondary:
# Se usa en relaciones many-to-many para indicar la tabla intermedia que conecta ambas tablas.


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]

    favorites: Mapped[list[Character]] = relationship(
        "Character",
        secondary=favorites_table,
        back_populates="favorited_by"
    )

    # back_populates
    # back_populates sincroniza ambas relaciones en los dos modelos.
    # Indica que la relación en una clase corresponde a la relación en la otra, creando así un vínculo bidireccional explícito.
    # Esto permite que, cuando cambias la relación en un lado (por ejemplo, asignas un padre a un hijo), automáticamente se actualice la relación inversa (el hijo queda en la lista de hijos del padre).

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [character.serialize() for character in self.favorites]
            # No incluimos password por seguridad
        }


# ¿Qué es pipenv run migrate y pipenv run upgrade?
# Cuando modificamos un modelo (por ejemplo, agregamos un campo nuevo, cambiamos una relación o creamos una tabla nueva), necesitamos reflejar esos cambios en la base de datos. Pero la base de datos es un sistema separado que no sabe nada de tu código, por eso usamos estas herramientas y comandos para sincronizarlos.

# 1. pipenv run migrate
# Este comando genera un archivo de migración automáticamente basado en los cambios que hiciste en los modelos.

# Una migración es como un conjunto de instrucciones (un script) que indica cómo cambiar la estructura de la base de datos (por ejemplo, crear una tabla, agregar una columna, modificar tipos, etc.).

# Es decir, con migrate detectas qué cambios hay y creas ese “plan” para actualizar la base.

# 2. pipenv run upgrade
# Este comando ejecuta las migraciones pendientes (los archivos generados con migrate) contra la base de datos real.

# Aplica esos cambios en la base de datos para que quede sincronizada con tus modelos en código.

# Sin este paso, la base de datos seguiría con la estructura vieja y no entendería los nuevos campos o tablas que definiste.

# ¿Por qué hay que hacer esto?
# Porque tus modelos en Python representan la estructura lógica de la base de datos.

# La base de datos física (el sistema que almacena datos) necesita que le digas cómo cambiar su estructura.

# Las migraciones permiten hacer estos cambios de forma controlada, versionada y segura, sin perder datos existentes.

# Así puedes evolucionar la base de datos sin borrarla ni hacerla manualmente, evitando errores y manteniendo todo sincronizado.