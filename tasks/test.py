""" Invoke collection -- test"""
from invoke import Collection, task


@task(default=True)
def test_all(ctx):
    """ Default task that runs linting for all python files"""
    # ctx.run("python -m unittest -v tests/**/test_*.py")
    ctx.run("pytest tests")


namespace = Collection("test")  # pylint: disable=invalid-name
namespace.add_task(test_all, "all")
