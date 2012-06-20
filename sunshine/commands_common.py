
import subprocess, shlex

class CommandError(Exception):
    def __init__(self, command, returncode, args):
        super(CommandError, self).__init__(
            'Command Error. Command: %s, Retcode: %d, Args: %s' %
            (command, returncode, args))

def get_output(command, args, ErrorClass=CommandError):
    """Excecutes a command and yields its standard output"""
    process = subprocess.Popen(_get_args(command, args), stdout=subprocess.PIPE)

    with process.stdout as stdout:
        for line in stdout:
            yield line

    process.wait()
    if process.returncode:
        raise ErrorClass(command, 1, args)


def call(command, args, ErrorClass=CommandError):
    """Exceutes a command and returns its return code"""
    retcode = subprocess.call(_get_args(command, args))
    if retcode:
        raise ErrorClass(command, retcode, args)

def _get_args(command, args):
    """ Function doc """
    return shlex.split(str(command + u' ' + u' '.join(args)))
