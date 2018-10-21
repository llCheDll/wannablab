import falcon
import jwt
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError
from .helpers import logout

from config import settings
from .constants import JWT_SECRET, JWT_ALGORITHM


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


class FalconAuthMiddleware(object):
    def __init__(self):
        self._unprotectedUri = [
            '/api/v1',
            '/api/v1/auth',
            '/api/v1/events',
            '/api/v1/users',
            '/api/v1/register'
        ]

    def process_request(self, request, response):
        if request.relative_uri not in self._unprotectedUri:
            token = request.get_header('Cookie')

            if token is None:
                raise falcon.HTTPUnauthorized()

            if self._token_is_valid(token, request, response):
                pass

    def _token_is_valid(self, token, request, response):
        jwt_token = token.split('=')[1]

        try:
            payload = jwt.decode(jwt_token, JWT_SECRET,
                                 algorithms=[JWT_ALGORITHM])

        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            logout(request, response)

        return True
