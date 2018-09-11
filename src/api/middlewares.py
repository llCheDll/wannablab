import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError

from config import settings


class DatabaseSessionManagerMiddleware(object):
    """
    Middleware class to provide access to database session in requests
    """

    def __init__(self, db_session):
        """
        Initializer

        :param db_session: manager to persistence operations for ORM-mapped objects
        :type db_session: falcon.Session
        """

        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, request, response, resource=None):
        """
        Handle post-processing of the response (after routing).

        :param request: client’s HTTP request (represented as object)
        :type request: falcon.Request
        :param response: HTTP response to a client request (represented as object)
        :type response: falcon.Response
        :param resource: RESTful falcon resource
        """

        request.context['session'] = self._session_factory()

    def process_response(self, request, response, resource=None):
        """
        Handle post-processing of the response (after routing).

        :param request: client’s HTTP request (represented as object)
        :type request: falcon.Request
        :param response: HTTP response to a client request (represented as object)
        :type response: falcon.Response
        :param resource: RESTful falcon resource
        """

        session = request.context['session']
        if settings.db_autocommit:
            try:
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise Exception()

        if self._scoped:
            session.rollback()
        else:
            session.close()
