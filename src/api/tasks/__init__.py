from invoke import Collection
from .runserver import runserver

ns = Collection('api')

ns.add_task(runserver)
