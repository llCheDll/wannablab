from invoke import Collection

from commons.tasks import shell

nc = Collection()
nc.add_task(shell)
