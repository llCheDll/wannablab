from invoke import Collection

from .dbshell import shell
from db.migrations.tasks.create import create
from db.migrations.tasks.upgrade import upgrade, downgrade
from .inserts import insert


ns = Collection('db')

ns.add_task(shell)
ns.add_task(create)
ns.add_task(upgrade)
ns.add_task(downgrade)
ns.add_task(insert)
