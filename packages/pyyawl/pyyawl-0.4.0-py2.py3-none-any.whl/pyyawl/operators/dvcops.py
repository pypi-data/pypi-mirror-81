__all__ = ['call_dvc_add', 'call_dvc_push', 'call_dvc_pull']

from pathlib import Path
from ..namedregistry import export
from .baseops import subprocess_run


@export(name='dvc_add', description='add the dataset to dvc', module=__name__)
def call_dvc_add(path: str, verbose: bool = False):
    result = subprocess_run(['dvc', 'add', path])
    if verbose:
        print('called dvc_add', path, result)
    return result


@export(name='dvc_push',
        description='push a dataset to a dvc repository',
        module=__name__)
def call_dvc_push(verbose: bool = False):
    result = subprocess_run(['dvc', 'push'])
    if verbose:
        print('called dvc_push', result)
    return result


@export(name='dvc_pull',
        description='pull all the dataset from the remote dvc repo',
        module=__name__)
def call_dvc_pull(verbose: bool = False):
    result = subprocess_run(['dvc', 'pull'])
    if verbose:
        print('called dvc_pull', result)
    return result