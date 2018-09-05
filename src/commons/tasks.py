from invoke import task


@task
def shell(ctx):
    """
    IPython shell
    """

    from IPython import start_ipython

    start_ipython(argv=[])
