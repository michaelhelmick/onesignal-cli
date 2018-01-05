import json
from os import makedirs
from os.path import expanduser, join

import click


class Config(dict):
    def __init__(self, *args, **kwargs):
        self.config = join(expanduser('~'), '.onesignal')

        try:
            makedirs(self.config)
        except OSError:
            pass

        self.config = join(self.config, 'config.json')

        super(Config, self).__init__(*args, **kwargs)

    def load(self):
        """Load a JSON config file from disk."""
        try:
            _config_file = open(self.config, 'r+')
            data = json.loads(_config_file.read())
        except (ValueError, IOError):
            data = {}

        self.update(data)

    def save(self):
        # self.config.ensure()
        _file = open(self.config, 'w+')
        _file.write(json.dumps(self))

    def _setup(self):
        auth_key = self.get('auth_key')

        if not auth_key:
            self['auth_key'] = click.prompt('Auth Key')
            self.save()


pass_config = click.make_pass_decorator(Config, ensure=True)
