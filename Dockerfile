FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN echo "Contenido de /app:" && ls -l /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "clasificador.app:app"]