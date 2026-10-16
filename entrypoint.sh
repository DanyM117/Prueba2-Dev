#!/bin/sh
set -e

echo "Iniciando servidor Nginx en el puerto 8080..."
nginx

echo "Iniciando backend Flask (Gunicorn) en 127.0.0.1:${PORT:-5000}..."
echo "Para probar la respuesta intentar entrar a http:/localhost:8080"
exec gunicorn \
    --bind "127.0.0.1:${PORT:-5000}" \
    --workers 1 \
    --capture-output \
    --enable-stdio-inheritance \
    --access-logfile - \
    --error-logfile - \
    app:app