from flask import Flask, Response
import os
import psycopg2
from zoneinfo import ZoneInfo
from datetime import datetime

app = Flask(__name__)

#Variables de environment
Nombre = os.getenv("NOMBRE", "No name")
puerto = int(os.getenv("PORT", "5000"))

#Variables de env para la bd Postrgres
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5,
    )

def registrar_en_bd(nombre: str, fecha: str) -> None:
    conn = get_db_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS log (
                        id SERIAL PRIMARY KEY,
                        nombre VARCHAR(255) NOT NULL,
                        fecha VARCHAR(100) NOT NULL
                    );
                    """
                )
                cur.execute(
                    "INSERT INTO log (nombre, fecha) VALUES (%s, %s);",
                    (nombre, fecha),
                )
    finally:
        conn.close()

@app.route("/")
def main_func():
    fecha = datetime.now(ZoneInfo("America/Monterrey")).strftime("%Y-%m-%d %H:%M:%S")
    message = f"Hello world! Nombre: {Nombre}, Fecha: {fecha}"

    #Insertamos el login en la tabla log
    try:
        registrar_en_bd(Nombre, fecha)
        print(f"{message} | [DB] INSERT exitoso en tabla 'log'", flush=True)
    except Exception as e:
        print(f"{message} | [DB ERROR] No se pudo insertar en 'log': {e}", flush=True)

    #Mostrar en LOG / systemout
    print(message, flush=True)
    #Mostrar en HTTP
    return Response(f"{message}\n", mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=puerto)