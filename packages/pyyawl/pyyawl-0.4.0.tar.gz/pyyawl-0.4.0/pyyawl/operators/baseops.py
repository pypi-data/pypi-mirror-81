__all__ = ['subprocess_run']

import subprocess
import platform


def subprocess_run(commands):
    if int(platform.python_version_tuple()[1]) == 6:
        return subprocess.run(commands, stdout=subprocess.PIPE)
    elif int(platform.python_version_tuple()[1]) > 6:
        return subprocess.run(commands, capture_output=True)
    else:
        raise Exception('python version not supported')
