import os
from invoke import Collection, task
from commons.tasks import shell

nc = Collection()
nc.add_task(shell)


@task
def runserver(ctx, host='127.0.0.1', port=8000):
    """
    Starts development server

    """
    from werkzeug.serving import run_simple
    from api.app import api

    subquote = 'Reloading' if 'WERKZEUG_RUN_MAIN' in os.environ else 'Starting'
    print(f'{subquote} development server at http://{host}:{port} ...')

    run_simple(host, port, api, use_reloader=True)