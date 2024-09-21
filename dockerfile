# Usamos una imagen de Ubuntu como base
FROM ubuntu:latest

# Actualizamos el sistema e instalamos las dependencias necesarias
RUN apt-get update && apt-get install -y python3 python3-pip default-libmysqlclient-dev build-essential pkg-config mysql-client libssl-dev

# Establecemos el directorio de trabajo en /APIRestHNP
WORKDIR /app

# Copy the current directory (our Flask app) into the container at /app
COPY . /app

ENV FLASK_APP=api.py

# Instalamos Django y mysqlclient
RUN pip3 install --break-system-packages Flask mysqlclient Flask-SQLAlchemy PyMySQL python-dotenv 

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
