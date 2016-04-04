import os

import click

from .utils import format_command, format_envvar


def run_command(config, name, args=None, env=None):
    if args is None:
        args = []

    # Prepare base environment
    base_env = (env if env is not None else os.environ).copy()

    cmd_spec = config.commands[name]

    # Prepare global environmnet
    global_env = _apply_replacements_dict(
        config.env, {'args': args, 'env': base_env})

    base_env.update(global_env)

    command_env = _apply_replacements_dict(
        cmd_spec.env, {'args': args, 'env': base_env})

    full_env = base_env.copy()
    full_env.update(command_env)

    run_args = _apply_replacements_list(
        cmd_spec.command, {'args': args, 'env': full_env})

    # No replacements applied on command-line arguments
    if cmd_spec.append_args:
        run_args.extend(args)

    extra_env = {}
    extra_env.update(global_env)
    extra_env.update(command_env)
    click.echo('\x1b[1m>\x1b[0m {}'.format(format_command(run_args)), err=True)
    for key, value in sorted(extra_env.items()):
        click.echo('  {}'.format(format_envvar(key, value)), err=True)

    os.execvpe(run_args[0], run_args, full_env)


def _apply_replacements(text, context):
    return text.format(*context['args'], **context)


def _apply_replacements_dict(obj, context):
    return {key: _apply_replacements(val, context)
            for key, val in obj.items()}


def _apply_replacements_list(obj, context):
    return [_apply_replacements(x, context) for x in obj]
