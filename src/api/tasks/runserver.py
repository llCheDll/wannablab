import sys
import subprocess
import time

from invoke import task

from config import settings


@task(help={"bind": "Bind to custom address or/and port. Default: localhost:8000"})
def runserver(ctx, bind=None):
    """
    Starts development server

    :param bind: host:port to run server
    :type bind: str
    """

    if bind:
        host, port = bind.split(':')
    else:
        host, port = settings.api.host, settings.api.port

    executable = 'gunicorn'

    args = [executable, 'api.app:app']
    args += ['-b', '{}:{}'.format(host, port)]
    args += ['--timeout', '600']
    args += ['--reload']

    try:
        subprocess.call(args)
    except KeyboardInterrupt:
        time.sleep(1)
        sys.exit(0)
