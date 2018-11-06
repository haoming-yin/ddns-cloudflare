""" Invoke collection -- root"""
from invoke import Collection
from tasks import test
from tasks import lint
from tasks import cloudflare

ns = Collection()  # pylint: disable=invalid-name

ns.add_collection(test.namespace)
ns.add_collection(lint.namespace)
ns.add_collection(cloudflare.namespace)
