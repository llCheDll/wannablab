from invoke import Collection

from api.tasks import ns as api_tasks
from commons.tasks import shell


ns = Collection()
ns.add_task(shell)

ns.add_collection(api_tasks)
