__all__ = ['call_echo']

from .baseops import subprocess_run
from ..namedregistry import export


@export(name='python',
        description='call a common python script',
        module=__name__)
def call_echo(value: str, verbose: bool = False):
    return subprocess_run(['python', value])
