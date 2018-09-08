from invoke import Collection, task
from commons.tasks import shell
from config import settings

nc = Collection()
nc.add_task(shell)


@task
def runserver(ctx, host=settings.api.host, port=settings.api.port):
    """
    Starts development server

    """
    from werkzeug.serving import run_simple
    from api.app import api

    print(f'Starting development server at http://{host}:{port} ...')

    run_simple(host, port, api, use_reloader=True)