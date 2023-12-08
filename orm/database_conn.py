from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(verbose=True)


class MyDb:
    db_engine = None
    db_url: str = environ.get("DB_URL", "mysql+pymysql://root:@localhost/agwise_api")
    debug_db = environ.get("DEBUG_DB", 0)
    if debug_db != 0:
        debug_db = True

    def __new__(cls, *args, **kwargs):
        if cls.db_engine is None:
            cls.db_engine = create_engine(
                url=cls.db_url,
                echo=cls.debug_db,
                echo_pool=cls.debug_db,
                hide_parameters=not cls.debug_db,
            )

        return cls.db_engine
