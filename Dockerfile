# Usa una imagen ligera de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del contexto al contenedor
COPY . /app

# Muestra el contenido para depuración (opcional, puedes quitarlo luego)
RUN echo "Contenido de /app:" && ls -l /app

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto por defecto de Gunicorn (Cloud Run usa el 8080)
EXPOSE 8080

# Comando para ejecutar la app usando Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8080 clasificador.app:app"]