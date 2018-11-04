""" Invoke collection -- test"""
from invoke import Collection, task


@task
def hello_world(ctx):
    """ Dummy task that prints 'hello world'"""
    ctx.run("echo Hello World!")


@task(default=True)
def test_all(_):
    """ Default task that runs linting for all python files"""
    pass


namespace = Collection("test")  # pylint: disable=invalid-name
namespace.add_task(hello_world)
