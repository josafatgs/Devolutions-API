import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

host = os.environ.get("DATABASE_HOST")
port = int(os.environ.get("DATABASE_PORT"))
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")
db = os.environ.get("DATABASE_NAME")