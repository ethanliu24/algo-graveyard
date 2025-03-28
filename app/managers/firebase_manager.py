import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join, dirname
from ..env_vars import ENV_VARS
from ..schemas.question import Question

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

    def get_all_questions(cls, collection: str) -> list[Question]:
        # TODO implement filter, use where() function
        docs = cls.db.collection(collection).stream()
        return [cls._format_doc(doc) for doc in docs]

    def get_question(cls, collection: str, id: str) -> Question:
        doc = cls.db.collection(collection).document(id).get()
        if not doc.exists:
            raise ValueError("Invalid question ID.")
        return Question(**doc.to_dict())

    def create_question(cls, question: dict, collection: str, id: str = None) -> str:
        collection = cls.db.collection(collection)
        if id:
            _, doc = collection.document(id).set(question)
        else:
            _, doc = collection.add(question)

        return doc.id

    def delete(cls, collection: str, id: str):
        cls.db.collection(collection).document(id).delete()

    def _format_doc(cls, doc) -> Question:
        return Question(**(doc.to_dict().update({ "id": doc.id })))
