Aliasfile
#########

Define your per-directory command aliases in Yaml, to get quick
shortcuts (and avoid having to remember long commands).

**WARNING:** This project is still experimental, and things may change
suddenly. Suggestions are welcome.


Configuration
=============

Configuration is held in a file, usually named ``./.aliases``, as a
dictionary serialized in YAML format.

The main section is ``commands``, a dict mapping alias names to their
specification.


Command specification
---------------------

- ``command``: command to be run, as a string

  - will be tokenized via ``shlex.split``
  - string-format-style placeholders will be replaced:

    - positional arguments (``{}``, ``{1}``) -> variadic arguments to the command
    - ..or explicit: ``{args[1]}``
    - environment: ``{env[USER]}``
    - vars (see below): ``{vars[USER]}``
    - extra arguments will be appended to the command

- ``env``: environment for the command

  - not considered in string formatting
  - will go through the same formatting as commands

- ``vars``: to be replaced in env/command formatting


Notes
=====

- we want some way to prevent automatic appending of varargs
- we might want to use jinja for formatting, so we can have conditionals / defaults
- we might want inheritance, rather than having "nested" aliasing


Examples
========

.. code-block:: yaml

    commands:
      test:
        command: xvfb-run py.test --reuse-db -vvv ./tests/
        env:
          DJANGO_SETTINGS_MODULE: fooproject.settings.testing
          PYTHONPATH: "{env[HOME]}/Projects/fooproject"

.. code-block:: yaml

    commands:
      manage:
        command: python manage.py
        env:
          DJANGO_SETTINGS_MODULE: fooproject.settings.testing
          PYTHONPATH: "{env[HOME]}/Projects/fooproject"
          LOG_LEVEL: DEBUG

      runserver:
        command: aliasfile manage runserver

      migrate:
        command: aliasfile manage migrate

      shell:
        command: aliasfile manage shell
