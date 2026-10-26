import os

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ImproperlyConfigured
from pymongo import ASCENDING, MongoClient
from bson import ObjectId

_client = None
_collection = None


def obtener_coleccion_usuarios():
    global _client, _collection

    uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONGODB_DATABASE")

    if not uri or not database_name:
        raise ImproperlyConfigured(
            "Configura MONGODB_URI y MONGODB_DATABASE."
        )

    if _collection is None:
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")

        _collection = _client[database_name]["usuarios"]
        _collection.create_index(
            [("cedula", ASCENDING)],
            unique=True,
        )

    return _collection


def crear_usuario(datos):
    documento = {
        "nombres": datos["nombres"],
        "apellidos": datos["apellidos"],
        "cedula": datos["cedula"],
        "edad": datos["edad"],
        "telefono": datos["telefono"],
        "contrasena": make_password(datos["contrasena"]),
    }

    return obtener_coleccion_usuarios().insert_one(documento)

def buscar_usuario_por_id(usuario_id):
    return obtener_coleccion_usuarios().find_one(
        {"_id": ObjectId(usuario_id)},
        {"contrasena": 0},
    )