from invoke import Collection

from .dbshell import shell


ns = Collection('db')

ns.add_task(shell)
