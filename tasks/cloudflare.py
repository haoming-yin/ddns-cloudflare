""" Invoke collection -- cloudflare """

from invoke import Collection, task
from helper import cloudflare


@task
def test(ctx):
    """ test"""

    ctx.run("echo finished cloudflare.te1st")


namespace = Collection("cf")  # pylint: disable=invalid-name
namespace.add_task(test)
