FROM python:3.13-slim

# Variables recomendadas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt e instala dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu aplicación Django
COPY . /app/

# Recopila los archivos estáticos (opcional para producción)
RUN python manage.py collectstatic --noinput

# Expone el puerto de Gunicorn
EXPOSE 8000

# Comando para ejecutar Gunicorn
CMD ["gunicorn", "Main.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]