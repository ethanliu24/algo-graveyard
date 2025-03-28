import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os.path import join, dirname
from ..env_vars import ENV_VARS
from ..schemas.question import Question, QuestionCreate

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

    def get_all_questions(cls) -> list[Question]:
        # TODO implement filter, use where() function
        docs = cls.db.collection(cls.question_collection).stream()
        return [cls._format_doc(doc) for doc in docs]

    def get_question(cls, id: str) -> Question:
        doc = cls.db.collection(cls.question_collection).document(id).get()
        if not doc.exists:
            raise ValueError("Invalid question ID.")
        return Question(**doc.to_dict())

    def create_question(cls, question: dict, id: str = None) -> str:
        collection = cls.db.collection(cls.question_collection)
        if id:
            _, doc = collection.document(id).set(question)
        else:
            _, doc = collection.add(question)

        return doc.id

    def _format_doc(cls, doc) -> Question:
        return Question(**(doc.to_dict().update({ "id": doc.id })))