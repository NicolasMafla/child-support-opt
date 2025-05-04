# Imagen base
FROM python:3.11-slim

# Instala dependencias del sistema necesarias para CBC y Streamlit
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Instala CBC (Coin-or Branch and Cut)
RUN wget https://github.com/coin-or/Cbc/releases/download/releases%2F2.10.12/Cbc-releases.2.10.12-x86_64-ubuntu20-gcc940-static.tar.gz \
    && tar -xvzf Cbc-releases.2.10.12-x86_64-ubuntu20-gcc940-static.tar.gz \
    && mv cbc /usr/local/bin/cbc \
    && chmod +x /usr/local/bin/cbc \
    && rm Cbc-releases.2.10.12-x86_64-ubuntu20-gcc940-static.tar.gz

# Crea el directorio de trabajo
WORKDIR /app

# Copia los archivos de la app
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Comando para iniciar la app
CMD streamlit run main.py --server.port=$PORT --server.enableCORS=false --server.enableXsrfProtection=false