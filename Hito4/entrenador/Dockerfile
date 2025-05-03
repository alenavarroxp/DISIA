FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para Pillow y OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Crear el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY requirements.txt .
COPY app.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Crear los volúmenes para datasets y salida de modelos
VOLUME ["/datasets", "/compartido"]

# Exponer el puerto del servidor Flask
EXPOSE 5000

# Comando de ejecución
CMD ["python", "app.py"]
