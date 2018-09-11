from alembic import command

from importlib import import_module
from invoke import task

from config import alembic_cfg


def prepare_models_and_get_alembic_config():
    """
    Loads all component models to be visible for alembic and creates
    component specific alembic config
    :param component_name:
    :return: alembic.config.Config instance
    """

    alembic_cfg.set_main_option(
        'file_template', '%%(year)d-%%(month).2d-%%(day).2d_%%(hour).2d-%%(minute).2d_%%(slug)s'
    )
    return alembic_cfg


@task(help={
    'message': 'The revision message',
    'strict': 'Raise if not all models placed in models/__init__.py file',
})
def create(ctx, message='', strict=True):
    """
    Creates a new revision file for given component
    """  # noqa

    # Check models availability from models/__init__.py
    module = import_module('db.models')
    class_registry = module.class_registry
    for classname, instance in class_registry.items():
        path = instance.__module__.split('.') # noqa

    alembic_config = prepare_models_and_get_alembic_config()
    command.revision(alembic_config, message=message, autogenerate=True)
