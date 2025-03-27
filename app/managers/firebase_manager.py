import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join, dirname
from ..env_vars import ENV_VARS

class FirebaseManager(object):
    _instance = None
    _db = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(FirebaseManager, cls).__new__(cls)

            if ENV_VARS.get("APP_ENV") == "production":
                if not firebase_admin._apps:
                    cred = credentials.Certificate(join(dirname(__file__), "..", "..", "firebase-key.json"))
            else:
                cred = credentials.Certificate(join(dirname(__file__), "..", "..", "firebase-key.json"))

            firebase_admin.initialize_app(cred)
            cls._db = firestore.client()

        return cls._instance
