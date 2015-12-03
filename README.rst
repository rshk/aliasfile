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
    - extra arguments will be appended to the command

- ``env``: environment for the command

  - replacements are applied on values, as with ``command``

- ``append_args``: boolean flag, indicating whether extra arguments on
  the command line should be automatically appended to
  ``command``. Defaults to ``True``; you might want to disable this if
  applying arguments manually using string formatting.


Notes
=====

- we might want to use jinja for formatting, so we can have
  conditionals / defaults
- it would be nice to handle "chained" alisaing internally, rather
  than doing multiple ``execvpe()`` calls


Examples
========

.. code-block:: yaml

    commands:
      test:
        command: py.test ./tests/
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
