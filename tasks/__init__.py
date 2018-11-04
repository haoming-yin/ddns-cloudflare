from invoke import Collection
from tasks import test

ns = Collection() # root namespace

ns.add_collection(Collection.from_module(test))