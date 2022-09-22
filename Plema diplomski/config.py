from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_marshmallow import Marshmallow
import os

#globalne promenljive
#relativn a putanja do ovog foldera
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
db = SQLAlchemy()
ma = Marshmallow()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "Pitanja.db")
