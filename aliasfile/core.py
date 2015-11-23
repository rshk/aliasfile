import os
import shlex

from .utils import _print_command


class Configuration:
    def __init__(self, commands=None, env=None, vars=None,
                 base_env=None):

        self.commands = commands or {}
        self.base_env = (base_env
                         if base_env is not None
                         else os.environ.copy())
        self.raw_env = env or {}
        self.raw_vars = vars or {}

    @classmethod
    def from_config(cls, config):
        return cls(
            commands={key: Command.from_config(cfg)
                      for key, cfg in config.get('commands', {}).items()},
            env=config.get('env', {}),
            vars=config.get('vars', {}))

    def run(self, args):
        cmd, *args = args
        self.commands[cmd].run(args)


class Command:
    def __init__(self, name, spec):
        self.name = name

        self.raw_command = []
        self.raw_env = {}
        self.raw_vars = {}

        if isinstance(spec, dict):
            self.raw_command = shlex.split(spec['command'])
            self.raw_env = spec.get('env') or {}
            self.raw_vars = spec.get('vars') or {}

        elif isinstance(spec, (str, bytes)):
            self.raw_command = shlex.split(spec)

        else:
            raise TypeError('Unsupported command spec type')

    def get_command(self, args):
        return [self._substitute(arg, args)
                for arg in self.raw_command] + args

    def get_env(self, args):
        return {key: self._substitute(val, args)
                for key, val in self.raw_env.items()}

    def get_vars(self, args):
        return {key: self._substitute(val, args, with_vars=False)
                for key, val in self.raw_vars.items()}

    def run(self, args):
        cmd = self.get_command(args)
        env = os.environ.copy()
        env.update(self.get_env(args))
        _print_command(cmd)

        os.execvpe(cmd[0], cmd, env)

    def _substitute(self, s, args, with_vars=True):
        context = {
            'env': os.environ,
            'args': args,
        }
        if with_vars:
            context['vars'] = self.get_vars(args)
        return s.format(*args, **context)
