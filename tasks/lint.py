""" Invoke collection -- lint"""
from invoke import task, Collection

DIRS = ["lib", "tasks"]


@task(help={"path": "Path that pylint runs against to."})
def lint_for(ctx, path="src"):
    """ Runs linting for the given path"""
    print(f"Running pylint for path: '{path}'")
    ctx.run(f"pylint {path} --load-plugins pylint_quotes")


@task(default=True)
def lint_all(ctx):
    """ Lints all python files"""
    for directory in DIRS:
        lint_for(ctx, directory)
    print("Finished pylint linting")


namespace = Collection("lint")  # pylint: disable=invalid-name
namespace.add_task(lint_all, name="all")
namespace.add_task(lint_for, name="for")
