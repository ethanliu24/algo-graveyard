import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import firestore
from os.path import join, dirname
from typing import Any
from ..env_vars import ENV_VARS

class FirebaseManager(object):
    client: Any  # should be Firebase Client type

    def __init__(self):
        env = ENV_VARS.get("APP_ENV")
        if env == "production" or env == "staging":
            if not firebase_admin._apps:
                # Assuming on Render
                cred = credentials.Certificate(
                    "/etc/secrets/firebase-key.json" if env == "production" else
                    join(dirname(__file__), "..", "..", "firebase-key.json")
                )
        else:
            cred = credentials.Certificate(join(dirname(__file__), "..", "..", "firebase-key.json"))

        firebase_admin.initialize_app(cred)
        self.client = firestore.client()

    def get_client(self):
        return self.client
