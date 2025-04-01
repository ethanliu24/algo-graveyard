class EntityNotFoundError(Exception):
    """ Raised when question ID is not found in the database. """
    def __init__(self, msg: str = None):
        super().__init__(msg if msg else "Invalid entity ID(s).")
