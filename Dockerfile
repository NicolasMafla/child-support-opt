# Imagen base
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    coinor-cbc \
    glpk-utils \
    && rm -rf /var/lib/apt/lists/*

# Crea el directorio de trabajo
WORKDIR /app

# Copia los archivos de la app
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Comando para iniciar la app
CMD streamlit run main.py --server.port=$PORT --server.enableCORS=false --server.enableXsrfProtection=false