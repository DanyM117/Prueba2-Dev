from flask import Flask, Response
import os
from zoneinfo import ZoneInfo
from datetime import datetime

app = Flask(__name__)

#Variables de environment
Nombre = os.getenv("Nombre", "No name")
puerto = int(os.getenv("PORT", "5000"))

@app.route("/")
def main_func():
    fecha = datetime.now(ZoneInfo("America/Monterrey")).strftime("%Y-%m-%d %H:%M:%S")
    message = f"Hello world! Nombre: {Nombre}, Fecha: {fecha}"

    #Mostrar en LOG / systemout
    print(message, flush=True)
    #Mostrar en HTTP
    return Response(f"{message}\n", mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=puerto)