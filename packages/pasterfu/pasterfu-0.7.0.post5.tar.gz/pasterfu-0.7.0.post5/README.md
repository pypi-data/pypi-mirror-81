# Pasterfu
Python program that opens a link with a command read from a database.

Made especially to use with RSS feed readers like newsboat. Or any other
program where you might want to open a specific in a manner based on the link
you are opening.

* Create a database according to your own needs
* Write a key that will match the whole link or just the beginning part of it
* List out commands you want to be run if mathing link is opened with pasterfu

Make a 'default' key into database to open unmatched links with commands listed
for the default key. You can have multiple databases and choose which one to
use with `--database` option.

> [Wiki][1] pages provide more in-depth information.

### Requirements

* Python 3.7 or newer
* [Pyperclip](https://github.com/asweigart/pyperclip) will be installed when
  installing pasterfu with pip
* In Ubuntu `sudo apt install python3`
* With Windows download and install [Python 3](https://www.python.org/)
  * You could consider selecting `Add Python to PATH` during install

### Install
1.  Install [Python 3](https://www.python.org/) - [Requirements][5]
2.  Run `pip install pasterfu`
3.  Create your config file rules. [Configuration][6]
    - For more info check [Wiki Configuration][3]
    - pasterfu will work with OS default browser even without configs

#### Linux
You propably need to use a command like:

```
pip3 install --upgrade pasterfu
```
Or:

```
python3 -m pip install --upgrade pasterfu
```

#### Windows
If you installed python without setting up path you need to include path when
running pip.

```
py.exe -m pip install --upgrade pasterfu
```

### Usage
```
pasterfu --link LINK
```

> Replace the "LINK" with the link you wish to open. Check
[Wiki Usage][4] for more info.

#### Windows
If you installed python without setting up path you need to include path when
running pasterfu.

For Python 3.8:
`%LOCALAPPDATA%\Programs\Python\Python38\Scripts\pasterfu.exe --link LINK`

### Configuration
* Create an empty database file in `~/.config/pasterfu.json`. Or in
`%USERPROFILE%\Documents\pasterfu.json` for Windows.

To add configurations run `pasterfu --add-rule 'key' --command
'command'`

* `key` what links to match for the rule
  * Make a "defalt" key that opens unmatched links
* `command` what to do if link is matching
  * `%link` can be used to pass the link for the command
  * Multiple commands can be set to a single key by separating the commands
    with `;`
  * Piped commands can be given, unfortunately currently only one pipe per
    command

> OS default internet browser will be used if no matching key is found and
> 'default' is not set.
>
> Read more at [Wiki Configuration][3].

#### Linux
##### Example 1
Open any link starting with `https://gitlab.com/` in Firefox:

```
pasterfu --add-rule https://gitlab.com/ --command "firefox %link"
```

##### Example 2
If no matching key is found write to key to file `~/link.txt` and open the link
with Firefox:

```
pasterfu --add-rule default --command "echo %link ; firefox %link"
```

##### Example 3
By using '%clip' you can copy a link with
[pyperclip](https://github.com/asweigart/pyperclip).

```
pasterfu --ad-rule https://gitlab.com/ --command "firefox %link ; %copy"
```
#### Windows
##### Example 4
Open gitlabs links in Brave:

```
pasterfu --add-rule https://gitlab.com/ --command
"C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe
%link"
```

##### Example 5
If no matching key is found open the link with Firefox:

```
pasterfu --add-rule default --command
"C:/Program Files/Mozilla Firefox/firefox.exe %link" ; C:/Program
Files/VideoLAN/VLC/vlc.exe"
```

##### Example 6
By using '%clip' you can copy a link with
[pyperclip](https://github.com/asweigart/pyperclip).

```
pasterfu --ad-rule https://gitlab.com/ --command
"C:/Program Files/Mozilla Firefox/firefox.exe %link ; %clip"
```

### Developing
TODO list found here [Wiki TODO][2]

Tests can be run with `./run_tests` or `run_tests.bat`. These require `flake8`
and `pytest`. Both can be found in [PyPI](https://pypi.org).

[1]: https://gitlab.com/noobilanderi/pasterfu/-/wikis/home
[2]: https://gitlab.com/noobilanderi/pasterfu/-/wikis/TODO
[3]: https://gitlab.com/noobilanderi/pasterfu/-/wikis/configuration
[4]: https://gitlab.com/noobilanderi/pasterfu/-/wikis/usage
[5]: https://gitlab.com/noobilanderi/pasterfu#requirements
[6]: https://gitlab.com/noobilanderi/pasterfu#configuration
