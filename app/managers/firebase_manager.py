import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join, dirname
from ..env_vars import ENV_VARS

class FirebaseManager(object):
    instance = None
    db = None

    def __new__(cls):
        if not cls.instance:
            # set up database
            cls.instance = super(FirebaseManager, cls).__new__(cls)

            if ENV_VARS.get("APP_ENV") == "production":
                if not firebase_admin._apps:
                    cred = credentials.Certificate(join(dirname(__file__), "..", "..", "firebase-key.json"))
            else:
                cred = credentials.Certificate(join(dirname(__file__), "..", "..", "firebase-key.json"))

            firebase_admin.initialize_app(cred)
            cls.db = firestore.client()

        return cls.instance

    def get_all(cls, collection: str):
        # TODO implement filter, use where() function
        return cls.db.collection(collection).stream()

    def get(cls, collection: str, id: str):
        return cls.db.collection(collection).document(id).get()

    def create(cls, data: dict, collection: str, id: str = None) -> str:
        collection = cls.db.collection(collection)
        if id:
            _, doc = collection.document(id).set(data)
        else:
            _, doc = collection.add(data)

        return doc.id

    def delete(cls, collection: str, id: str):
        cls.db.collection(collection).document(id).delete()

    def update(cls, collection: str, id: str, data: dict):
        cls.db.collection(collection).document(id).update(data)
