from sqlalchemy import inspect

from app.database.connection import engine


def actualizar_base_datos():
    inspector = inspect(engine)

    columnas = [
        columna["name"]
        for columna in inspector.get_columns("estadias")
    ]

    with engine.begin() as conexion:

        if "suscripcion_id" not in columnas:
            conexion.exec_driver_sql(
                "ALTER TABLE estadias "
                "ADD COLUMN suscripcion_id INTEGER "
                "REFERENCES suscripciones(id)"
            )
            print("Columna suscripcion_id agregada.")

        if "modalidad" not in columnas:
            conexion.exec_driver_sql(
                "ALTER TABLE estadias "
                "ADD COLUMN modalidad VARCHAR(10)"
            )
            print("Columna modalidad agregada.")

    print("Actualizacion de base de datos finalizada.")


if __name__ == "__main__":
    actualizar_base_datos()