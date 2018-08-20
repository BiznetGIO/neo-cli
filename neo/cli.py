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
from docopt import docopt, DocoptExit
from neo import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import neo.clis
    options = docopt(__doc__, version=VERSION, options_first=True)
    command_name = ""
    args = ""
    command_class =""

    command_name = options.pop('<command>')
    args = options.pop('<args>')

    if args is None:
        args = {}

    try:
        module = getattr(neo.clis, command_name)
        neo.clis = getmembers(module, isclass)
        command_class = [command[1] for command in neo.clis
                   if command[0] != 'Base'][0]
    except AttributeError as e:
        print(e)
        raise DocoptExit()

    command = command_class(options, args)
    command.execute()


if __name__ == '__main__':
    main()
