objclick
========

[![pypi](https://img.shields.io/pypi/v/objclick.svg)](https://pypi.org/project/objclick) [![python versions](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/) [![documentation](https://img.shields.io/badge/documentation-latest-success)](https://embray.gitlab.io/objclick) [![pipeline status](https://gitlab.com/embray/objclick/badges/master/pipeline.svg)](https://gitlab.com/embray/objclick/badges/master/pipeline.svg)

`objclick` provides a drop-in replacement for
[click](https://click.palletsprojects.com/en/7.x/), extending it to work in
various OOP contexts.

`click` is a very nice package for quickly and easily defining composable
command-line interfaces in a declarative manner by stacking decorators on
top of functions that implement the "main" functions of a commands.

However, by design, it does not play well in OOP contexts.  In particular,
it is not so easy to promote an instance method of a class to a `click`
command.  This package attempts to rectify that by providing wrappers around
`click` that also play well with classes in some cases.

To give a motivating example, say you have a base class that implements a
CLI:

```python
>>> import objclick as click
>>> import abc
>>> class BaseService(metaclass=abc.ABCMeta):
...     def explain(self):
...         """Explain this service; must be implemented by subclasses."""
...
...     @click.command()
...     def main(self):
...         print('Hello, let me tell you about myself.')
...         self.explain()
...

```

This class must now be subclassed with an implementation of `explain`, but
the subclass need not re-implement the rest of the CLI:

```python
>>> class MyService(BaseService):
...     def explain(self):
...         print(f'I am an instance of {self.__class__.__name__}.')
...

```

Since `MyService.main` is an instance method, we cannot simply call
`MyService.main()` to run the "main" function of CLI.  Just like with a
normal instance method of a class, we must instantiate the class first and
call the method on the instance:

```python
>>> service = MyService()
>>> service.main([], standalone_mode=False)
Hello, let me tell you about myself.
I am an instance of MyService.

```

(note:
[standalone_mode](https://click.palletsprojects.com/en/7.x/api/?highlight=standalone_mode#click.BaseCommand.main)
is a standard argument to `click` main functions that is useful for testing
commands.)

The inititial version of this package is still experimental, but it
implements a number of other useful cases.

One such case is given by the `classgroup` decorator.  This allows defining
a command group on a classmethod-like method that is bound to the class
rather than an instance of the class.  In the common case where a
classmethod implements an alternative constructor for a class, if the
classgroup returns an *instance* of the class it's define on, this instance
will be passed as the `self` argument to any instance methods that are added
as subcommands of the group.

For example, here is command group that takes a `--config` option, as a
configuration is needed to instantiate the `Service` class.  All subcommands
of `Service.main` can then access the configuration:

```python
>>> import objclick as click
>>> import json, pprint
>>> class Service:
...     def __init__(self, config):
...         """Instantiate `Service` with a configuration dict."""
...
...         self.config = config
...
...     @click.classgroup()
...     @click.option('--config', type=click.File())
...     def main(cls, config=None):
...         if config is not None:
...             with config as f:
...                 config = json.load(f)
...         else:
...             config = {}
...
...         print(f'Starting up {cls.__name__}...')
...         return cls(config)
...
...     @main.command()
...     def show_config(self):
...         print('Config:', end=' ')
...         pprint.pprint(self.config)
...

```

Now the CLI defined by `Service` can be invoked like:

```python
>>> import tempfile
>>> config = {'option1': 'a', 'option2': 'b'}
>>> with tempfile.NamedTemporaryFile(mode='w') as f:
...     json.dump(config, f)
...     f.flush()
...     # like `service.py --config <config-file> show-config`
...     args = ['--config', f.name, 'show-config']
...     Service.main(args, standalone_mode=False)
...
Starting up Service...
Config: {'option1': 'a', 'option2': 'b'}

```
