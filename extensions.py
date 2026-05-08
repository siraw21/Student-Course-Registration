from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = SQLAlchemy()
        return cls._instance


# Create the single instance — every import gets this same object
_db_singleton = DatabaseManager()

db = _db_singleton.db
migrate = Migrate()

