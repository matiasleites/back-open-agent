# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias primero (mejor cache)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto que usará Cloud Run
EXPOSE 8080

# Variable de entorno para Google Cloud Run
ENV PORT=8080

# Si usas variables de entorno como FIREBASE_SERVICE_ACCOUNT_PATH, configúralas en Cloud Run

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]