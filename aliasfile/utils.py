"""Misc utility functions
"""

import re

import click


def _print_command(args):
    """Nicely prints a command to console

    Args:
        args: command, as a list / tuple
    """
    click.echo('\x1b[1m>\x1b[0m \x1b[34m{}\x1b[0m'
               .format(_format_command(args)))


def _format_command(args):
    """Nicely format a command for printing.

    Will apply escaping when needed

    Args:
        args: command, as a list / tuple
    """

    return ' '.join(_escape_argument(a) for a in args)


def _escape_argument(text):
    """Escape a command argument
    """

    re_no_need_escaping = re.compile(r'^[0-9a-zA-Z_\.-]+$')
    if re_no_need_escaping.match(text):
        return text

    replacements = {
        '\\': '\\\\',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '"': '\\"',
    }

    def _escape_char(char):
        if char in replacements:
            return replacements[char]
        return char

    return '"{}"'.format(''.join(_escape_char(x) for x in text))
