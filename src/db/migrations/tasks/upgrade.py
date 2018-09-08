from alembic import command
from invoke import task

from config import alembic_cfg


@task(help={'revision': 'Revision id (default: "head", eg. 38c25174a395)'})
def upgrade(cfg, revision='head', *args, **kwargs):
    """Upgrades to a later version.

Usage: invoke db.migrations.upgrade -r 38c25174a395"""
    command.upgrade(config=alembic_cfg, revision=revision)


@task(help={
    'revision': 'Revision to which migrations will be downgraded (default: -1).'
})
def downgrade(cfg, revision='-1'):
    """
    Reverts to a previous or specified revision.

    Usage:
        invoke db.migrations.downgrade -r 48ec92753b6a  Will downgrade to revision 48ec92753b6a.
        invoke db.migrations.downgrade                  Will downgrade to previous revision.
    """

    command.downgrade(alembic_cfg, revision)
