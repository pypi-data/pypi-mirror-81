#! /usr/bin/env python3


"""API for libfu.

Combines objects and methods from libfu.py into singular objects that
are easier to implement into runner scripts.

OpenLink: Contains methods and data needed for opening a link.
RunDatabase: Methods and data for running database actions.
"""


import pyperclip
import subprocess
import webbrowser
import json
import re
from . import libfu


class OpenLink():
    """Contains methods and data needed for opening a link."""

    def check_regex(self, link):
        """Return link if it matches regex."""

        regex_url = re.compile(
            r'^http(s)?://(www\.)?'
            r'(\w+\.){1,2}(\w)+'
            r'(/[a-zA-Z0-9-+.@#/&%?~_=]*)?$')

        if regex_url.fullmatch(link):
            self.__link = link
        else:
            raise ValueError("name 'link' failed regex check")

    def load_ruleset(self, path=False):
        """Ruleset dictionary into instance variable.

        Loads data from given path or from default path.
        Creates RuleObjects() from each 'key': 'value' pair.
        Arrange pairs into RulesetObject().
        Return dictionary with RulesetObject().get_ruleset().
        """

        db = libfu.DatabaseErrCheck(path)
        data = db.load()
        if data:
            self.__data = data
        else:
            print('no data found in file')
            webbrowser.open(self.__link)
            return False

        rule_list = []
        for key in self.__data:
            rule_list.append(libfu.RuleObject(key, self.__data[key]))

        rules = libfu.RulesetObject(rule_list)

        if rules:
            self.__ruleset = rules.get_ruleset()
            return True
        else:
            print('could not create rulest from data')
            webbrowser.open(self.__link)
            return False

    def link2key(self):
        """Search for key that fits for the link.

        Store default Key ID if one is found.
        Use default if no 'key in link' match is found.
        Otherwice return False.
        """

        default = False

        for i, key in enumerate(self.__ruleset):
            if key in self.__link:
                self.__key = key
                return True
            elif 'default' in key:
                default = i
        else:
            if default:
                self.__key = 'default'
                return True
            else:
                print(f'no fitting key found for {self.__link}')
                webbrowser.open(self.__link)
                return False

    def process_cmd(self):
        """Process link variables.

        Return false if commands are empty for key.
        """

        comms = self.__ruleset[self.__key]
        if not comms:
            print(f'commands list empty for {self.__key}')
            webbrowser.open(self.__link)
            return False

        commands = []
        for comm in comms:
            if comm == ['%clip']:
                pyperclip.copy(self.__link)
                continue
            command = [c.replace('%link', self.__link) for c in comm]
            commands.append(command)

        self.__commands = commands
        return True

    def run_pipe(self):
        """Run piped command.

        Split command from pipe.

        Run first part and output results into the second one.
        """

        c = self.__pipe_cmd
        i_pipe = c.index('|')

        pre = c[:i_pipe]
        post = c[i_pipe+1:]

        pre = subprocess.Popen(pre, stdout=subprocess.PIPE)
        post = subprocess.check_output(post, stdin=pre.stdout)

    def run_cmds(self):
        """Runs the link opening command.

        Check if pipes are found and use run_pipe() accordingly.
        """

        for c in self.__commands:
            pipes = c.count('|')
            if pipes == 0:
                subprocess.run(c)
            elif pipes == 1:
                self.__pipe_cmd = c
                self.run_pipe()
            else:
                print('more than one pipe found in command')
                webbrowser.open(self.__link)
                return


class RunDatabase():
    """Methods and data for running database actions."""

    @staticmethod
    def prompt_user(prompt, retry=2, remind='Invalid input'):
        """Prompt user for confirmation."""

        while True:
            check = input(prompt)
            if check in ('y', 'yes', 'Y', 'YES'):
                return True
            if check in ('n', 'no', 'N', 'NO'):
                return False
            retry = retry - 1
            if retry < 0:
                raise ValueError('invalid user response')
            print(remind)

    @staticmethod
    def ruleset_values(ruleset, i, x):
        """Print ruleset dictionary content for call_dict()."""

        def json_markings(i, listing, line):
            """Print character ',' in json compliant manner."""

            if i+1 is len(listing):
                p_line = line
            else:
                p_line = f'{line},'

            print(p_line)

        print(f'    "{x}":')
        print('        [')
        for b, y in enumerate(ruleset[x]):
            cmd_end = f'            {y}'
            json_markings(b, ruleset[x], cmd_end)
        else:
            key_end = '        ]'
            json_markings(i, ruleset, key_end)

    def load_database(self, path):
        """Load database file into ruleset object."""

        db = libfu.Database(path)
        self.__path = db.absolute(path)
        data = db.load()
        rule_list = []

        if not data:
            print('working with an empty database file')
            self.__rules = libfu.RulesetObject(rule_list)
            return
        else:
            for key in data:
                rule_list.append(libfu.RuleObject(key, data[key]))
            rules = libfu.RulesetObject(rule_list)

        self.__ruleset = rules.get_ruleset()
        self.__rules = rules

    def call(self):
        """Prints ruleset and shows Key and Command ID's."""

        ruleset = self.__rules.get_ruleset()
        for i, x in enumerate(ruleset):
            print(f'Key #{i}: "{x}"')
            for j, y in enumerate(ruleset[x]):
                print(f'    Cmd #{j}: "{y}"')
            print()

    def call_dict(self):
        """Prints ruleset in a json compliant dictionary format.

        You could redirect stdout into file.
        """

        ruleset = self.__rules.get_ruleset()
        print('{')
        for i, x in enumerate(ruleset):
            self.ruleset_values(ruleset, i, x)
        print('}')

    def call_json(self):
        """Prints ruleset in a json format.

        You could redirect stdout into file.
        """

        ruleset = self.__rules.get_ruleset()
        print(json.dumps(ruleset, indent=4))

    def add_rule(self, key, command):
        """Add a new rule into ruleset."""

        self.__rules.add(key, command)

    def remove_rule(self, key):
        """Remove a rule from ruleset."""

        self.__rules.remove(key)

    def add_commands(self, command, id_k):
        """Add a command into a rule."""

        rule = self.__rules.find_rule(id_k)
        rule.add(command)

    def edit_commands(self, command, id_k, id_c):
        """Edit commands from a rule."""

        rule = self.__rules.find_rule(id_k)
        rule.edit(command, id_c)

    def remove_command(self, id_k, id_c):
        """Remove command from a rule.

        The last command currently cannot be removed.
        Instead use remove_rule() if you wish to remove the whole rule.
        """

        rule = self.__rules.find_rule(id_k)
        rule.remove(id_c)

    def write(self):
        """Write ruleset changes back into database file."""

        ask = 'Do you want to write the changes back to database? y/n\n'
        if not self.prompt_user(ask):
            return

        ruleset = self.__rules.get_ruleset()
        with open(self.__path, 'w') as o_file:
            json.dump(ruleset, o_file)
