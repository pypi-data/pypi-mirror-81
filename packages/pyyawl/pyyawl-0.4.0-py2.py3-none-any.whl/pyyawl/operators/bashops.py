__all__ = ['call_echo', 'call_mkdir', 'call_rmdir', 'call_ls']

from pathlib import Path
import shutil
from ..namedregistry import export
from .baseops import subprocess_run


@export(name='echo', description='call the echo command', module=__name__)
def call_echo(value: str, verbose: bool = False):
    """call the echo command

    Args:
        value (str): the value printed
        verbose (bool, optional): if True returns additional information. Defaults to False.

    Returns:
        Any: the response of the call
    """
    result = subprocess_run(['echo', 'hello', value])
    if verbose:
        print(result)
    return result


@export(name='mkdir', description='call the mkdir command', module=__name__)
def call_mkdir(path: str, verbose: bool = False):
    path = Path(path)
    return path.mkdir(parents=True, exist_ok=True)


@export(name='rmdir', description='call the rmdir command', module=__name__)
def call_rmdir(path: str, force: bool = False, verbose: bool = False):
    return shutil.rmtree(path, True, None)


@export(name='ls', description='call the ls command', module=__name__)
def call_ls(path: str, verbose: bool = False):
    path = Path(path)
    result = list(path.iterdir())
    print(result)
    return result
