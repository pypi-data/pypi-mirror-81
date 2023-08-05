#! /usr/bin/env python3


"""Library file for pasterfu.

Contains the framework objects needed for using pasterfu.

Rulings: provides methods that RulesetObject and RuleObject need.
RulesetObject: combines RuleObjects into one class and governs them.
RuleObject: individual 'key': 'value' parings and methods for them.
Database: loading ruleset data from file
DatabaseErrCheck: adds error handling for Database for link running.
"""


import os
import json
from pathlib import Path


class Rulings():

    @staticmethod
    def match(y, x):
        """Returns ID if given list has the ID value."""

        for i, value in enumerate(y):
            if i == x:
                return i
        else:
            raise ValueError(f'invalid value id {x}')

    @staticmethod
    def into_commands(command):
        """Generates commands list from a command string.

        'command parameter ; command'
        [['command', 'parameter'], ['command']]
        """

        return [c.split() for c in command.split(';')]


class RulesetObject(Rulings):
    """Collection of the {"key": [["value"]]} pair rules."""

    def __init__(self, ruleset):
        self.__ruleset = ruleset

    def find_rule(self, id_k):
        i = self.match(self.__ruleset, id_k)
        return self.__ruleset[i]

    def get_ruleset(self):
        """Returns the ruleset as a dictionary."""

        ruleset = {}
        for rule in self.__ruleset:
            get = rule.get_rule
            ruleset[get()[0]] = get()[1]
        return ruleset

    def add(self, key, command):
        """Add a rule object into ruleset."""

        commands = self.into_commands(command)
        self.__ruleset.append(RuleObject(key, commands))

    def remove(self, id_k):
        """Remove rule object from ruleset.

        Use staticmethod match to find rule from ruleset.
        """

        i = self.match(self.__ruleset, id_k)
        self.__ruleset.remove(self.__ruleset[i])

    def __repr__(self):
        return f"Ruleset('{self.__ruleset}')"


class RuleObject(Rulings):
    """URL to match paired with commands to run it with."""

    def __init__(self, key, command):
        self.__key = key
        self.__commands = command

    def add(self, command):
        """Add new commands for rule."""

        commands = self.into_commands(command)
        for comm in commands:
            self.__commands.append(comm)

    def remove(self, id_c=0):
        """Remove command from rule.

        Use staticmethod match to find command from rule.
        """

        i = self.match(self.__commands, id_c)
        if len(self.__commands) <= 1:
            raise ValueError(
                'cannot remove the last command from a key, use'
                '--remove-rule to remove the whole key:value pair')
        else:
            self.__commands.remove(self.__commands[i])

    def edit(self, command, id_c=0):
        """Edit commands from rule.

        Use staticmethod into_commands to generate commands list.
        """

        commands = self.into_commands(command)
        for x, command in enumerate(commands):
            i = self.match(self.__commands, id_c + x)
            self.__commands[i] = command

    def get_rule(self):
        """Returns rule attributes."""

        return [self.__key, self.__commands]

    def __repr__(self):
        return f"Rule('{self.__key}', '{self.__commands}')"


class Database():

    """Loads up json database."""

    __db = {
        'posix': '~/.config/pasterfu.json',
        'nt': '~/Documents/pasterfu.json'}

    def __init__(self, path=False):
        """Set path if one given, otherwice sets OS default path."""

        self.__path = self.absolute(path)

    def absolute(self, path):
        """Returns absolute path if it exists."""

        if not path:
            path = self.__db[os.name]

        p = Path.resolve(Path.expanduser(Path(path)))

        if Path.exists(p):
            return p
        else:
            raise FileNotFoundError(f"No such file or directory: '{p}'")

    def load(self, path=False):
        """Read ruleset from database."""

        if not path:
            path = self.__path

        if Path.stat(path).st_size == 0:
            rules = {}
            return rules

        with open(path) as db:
            rules = json.load(db)
        return rules

    def write(self, ruleset):
        """Write ruleset back to database."""

        with open(self.__path, 'w') as o_file:
            json.dump(ruleset, o_file)

    def __repr__(self):
        return (f"Database('{self.__path}')")


class DatabaseErrCheck(Database):
    """Changes to Database class for running links."""

    def __init__(self, path=False):
        """Replace patch checking and load with error handled methods."""

        self.absolute = self.err_check_path(self.absolute, path)
        self.__path = self.absolute(path)
        self.load = self.err_check_load(self.load)

    def err_check_path(self, orig_func, path):
        """Parent class method absolute with error handling."""

        def wrapper_path(path):
            """Add error handling to database path finding."""

            try:
                p = orig_func(path)
            except FileNotFoundError as err:
                print(f'FileNotFoundError: {err}')
                return False
            return p
        return wrapper_path

    def err_check_load(self, orig_func):
        """Load database with error handling for running links."""

        def wrapper_load():
            """Add error handling to load method."""

            if self.__path:
                try:
                    rules = orig_func(self.__path)
                except json.decoder.JSONDecodeError as err:
                    print(f'json.decoder.JSONDecodeError: {err}')
                    return False
                except TypeError as err:
                    print(f'TypeError: {err}')
                    return False
                return rules
            else:
                return False

        return wrapper_load
