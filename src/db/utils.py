from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import settings


def get_engine(db_uri, options=None):
    """
    Get database engine.
    :param db_uri: database uri, e.g. <database engine>://<user>:<password>@<host>/<database name>
    :type db_uri: basestring
    :param options: options like pool_recycle, pool_size, autocommit, etc.
    :type options: dict
    :return: database engine object
    """

    if not options:
        options = {}

    return create_engine(db_uri, **options)


engine = get_engine(settings.db.master.dsn)
session = scoped_session(sessionmaker())

_session_init = False


def init_session(force=False):
    """
    Database session init
    """

    global _session_init, session, engine
    if _session_init and not force:
        return session
    _session_init = True
    session.configure(bind=engine)
    return session


def create_session(db_uri, engine_options=None, session_options=None, create_all=False):
    """
    Create database session.

    :param db_uri: database uri, e.g. <database engine>://<user>:<password>@<host>/<database name>
    :type db_uri: basestring
    :param engine_options: options
    :type engine_options: dict
    :param session_options: options
    :type session_options: dict
    :param create_all:
    :return: database session object
    """

    from db.models import Base

    if not engine_options:
        engine_options = {}

    db_engine = create_engine(db_uri, **engine_options)

    if not session_options:
        session_options = {}

    session_options.update({
        'bind': db_engine
    })
    db_session = scoped_session(sessionmaker(**session_options))
    if create_all:
        Base.metadata.create_all(db_engine)

    return db_session


def get_new_session(engine_options=None, session_options=None, create_all=False):
    return create_session(
        settings.db.master.dsn,
        engine_options,
        session_options,
        create_all
    )
