import click
import yaml

from .core import Command


def list_commands(config):
    click.echo('Available commands:')
    for name, cmd in sorted(config.get('commands', {}).items()):
        click.echo('    \x1b[1m{}\x1b[0m'.format(name))


@click.command()
@click.option('--config', 'config_filename', default='.aliases')
@click.argument('args', nargs=-1)
def main(config_filename, args):
    with open(config_filename, 'r') as fp:
        config = yaml.load(fp)

    if len(args) < 1:
        return list_commands(config)

    cmd_name, *pos_args = args

    spec = config['commands'][cmd_name]
    cmd = Command(cmd_name, spec)
    cmd.run(pos_args)
