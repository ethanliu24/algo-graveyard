import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import firestore
from os.path import join, dirname
from ..env_vars import ENV_VARS

class FirebaseManager(object):
    def __init__(self):
        if ENV_VARS.get("APP_ENV") == "production":
            if not firebase_admin._apps:
                cred = credentials.Certificate(join(dirname(__file__), "..", "..", "firebase-key.json"))
        else:
            cred = credentials.Certificate(join(dirname(__file__), "..", "..", "firebase-key.json"))

        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_client(self):
        return self.client
