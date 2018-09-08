from invoke import Collection

from api.tasks import ns as api_tasks
from commons.tasks import shell
from db.tasks import ns as db_tasks


ns = Collection()
ns.add_task(shell)

ns.add_collection(api_tasks)
ns.add_collection(db_tasks)
