#! /usr/bin/env python3


"""Command Line Interface for pasterfu.

Using libfu_api to access libfu methods.
"""


import argparse
from . import constants
from . import libfu_api


class Arguments():
    """Argparse methods for running pasterfu in CLI."""

    def __init__(self):
        """Initialize the arguments."""

        args = self.get_opts()
        if args:
            self.__args = args

    def get_opts(opts):
        """Argparse settings."""

        parser = argparse.ArgumentParser(argument_default=False)
        parser.add_argument(
            '-v', '--version', help='show pasterfu version',
            action='store_true')
        parser.add_argument(
            '-l', '--link', help="""give link to open it with commands that
            are specified in the chosen database""")
        parser.add_argument(
            '-c', '--call', help='print the current database rules',
            action='store_true')
        parser.add_argument(
            '-t', '--call-dict', help="""print the current database as a
            dictionary, useful if you wish to manually edit rules""",
            action='store_true')
        parser.add_argument(
            '-j', '--call-json', help="""print the current database as a json
            dictionary, also useful if you wish to manually edit rules""",
            action='store_true')
        parser.add_argument(
            '-d', '--database', help='give path to a custom database')
        parser.add_argument(
            '--add-rule', help='make a new rule for the database')
        parser.add_argument(
            '--remove-rule', help="""remove rule from the database, use
            --id-key to specify which rule to remove""", type=int)
        parser.add_argument(
            '--add-commands', help="""add new commands into an existing rule,
            use --id-key to specify which rule to add the command, use
            --command to give the command to add""", type=int)
        parser.add_argument(
            '--edit-commands', help="""edit commands from rule --command give
            new commands --database edit custom database""", type=int)
        parser.add_argument(
            '--remove-command', help="""remove command from rule --id to
            specify which command to remove""", type=int)
        parser.add_argument(
            '--command', help="""give new command for ruleset, use with
            --edit-commands or""")
        parser.add_argument(
            '-i', '--id', help='number of the command to edit or remove',
            type=int)
        args = parser.parse_args()

        return args

    def open_link(self):
        """Open given link.

        Open link with webbrowser if one of the methods fail.
        """

        run = libfu_api.OpenLink()
        run.check_regex(self.__args.link)

        if not run.load_ruleset(self.__args.database):
            return

        if not run.link2key():
            return

        if not run.process_cmd():
            return

        run.run_cmds()

    def run_args(self):
        """Run the program with arguments."""

        args = self.__args

        if args.version is not False:
            print(f'{constants.__version__}')
            return

        # libfu.Runner
        if args.link is not False:
            self.open_link()
            return

        # libfu.Rules
        if args.call is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.call()
        elif args.call_dict is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.call_dict()
        elif args.call_json is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.call_json()
        elif args.add_rule is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.add_rule(args.add_rule, args.command)
            db.call()
            db.write()
        elif args.remove_rule is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.remove_rule(args.remove_rule)
            db.call()
            db.write()
        elif args.add_commands is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.add_commands(args.add_commands, args.command)
            db.call()
            db.write()
        elif args.edit_commands is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.edit_commands(args.command, args.edit_commands, args.id)
            db.call()
            db.write()
        elif args.remove_command is not False:
            db = libfu_api.RunDatabase()
            db.load_database(args.database)
            db.remove_command(args.remove_command, args.id)
            db.call()
            db.write()


def main():
    """The main function of pasterfu cli."""

    args = Arguments()
    args.run_args()
