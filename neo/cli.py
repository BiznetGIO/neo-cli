"""
Usage:
  neo <command> [<args>...]

Options:
      --config string                    Location of client config
  -h, --help                             display this help and exit
  -v, --version                          Print version information and quit

Commands:
  attach      Attach local standard input, output, and error streams to a running machine
  create      Deploying neo stack
  login       Log in to a NEO Cloud
  logout      Log out from a NEO Cloud
  ls          List all stack, network, machine
  rm          Delete stack, network, machine
  update      Update neo stack

Run 'neo COMMAND --help' for more information on a command.
"""

from inspect import getmembers, isclass
from docopt import docopt
# from docopt import DocoptExit
from neo import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import neo.clis
    options = docopt(__doc__, version=VERSION, options_first=True)
    # Retrieve the command to execute.
    command_name = ""
    args = ""
    command_args = ""
    command_args2 = ""

    for (k, v) in options.items():
        if k == '<command>' and v:
            command_name = options['<command>']
        if k == '<args>' and v:
            args = options['<args>']

    if not args:
        command_args = None
    else:
        command_args = args[0]
        if len(args) > 1:
            command_args2 = args[1]

    if hasattr(neo.clis, command_name) and command_name != '':
        module = getattr(neo.clis, command_name)
        neo.clis = getmembers(module, isclass)
        command = [command[1] for command in neo.clis
                   if command[0] != 'Base'][0]
        if command_args2 != '':
            command = command(options, command_args, command_args2)
        else:
            command = command(options, command_args)
        command.execute()


if __name__ == '__main__':
    main()
