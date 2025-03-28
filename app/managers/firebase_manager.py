import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join, dirname
from ..env_vars import ENV_VARS
from ..schemas.question import Question

class FirebaseManager(object):
    instance = None
    db = None
    question_collection = None

    def __new__(cls, question_collection: str):
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

            # set up db variables
            cls.question_collection = question_collection

        return cls.instance

    def get_questions(cls) -> list[Question]:
        # TODO implement filter, use where() function
        docs = cls.db.collection(cls.question_collection).stream()
        return [Question(**doc.to_dict()) for doc in docs]
