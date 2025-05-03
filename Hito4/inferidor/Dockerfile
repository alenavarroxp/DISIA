FROM python:3.10-slim

# Instalar dependencias necesarias del sistema (para Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY app.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Asegurar que la carpeta compartida del volumen esté accesible
VOLUME ["/compartido"]

# Exponer el puerto que utiliza Flask
EXPOSE 5001

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
