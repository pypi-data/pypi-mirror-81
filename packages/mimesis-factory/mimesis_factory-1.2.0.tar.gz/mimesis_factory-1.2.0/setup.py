# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mimesis_factory']
install_requires = \
['factory-boy>=2.11,<4.0', 'mimesis>=4.0,<5.0']

setup_kwargs = {
    'name': 'mimesis-factory',
    'version': '1.2.0',
    'description': 'Mimesis integration with factory_boy',
    'long_description': '## mimesis_factory\n\n[![Build Status](https://travis-ci.com/mimesis-lab/mimesis-factory.svg?branch=master)](https://travis-ci.com/mimesis-lab/mimesis-factory)\n[![Coverage](https://coveralls.io/repos/github/mimesis-lab/mimesis-factory/badge.svg?branch=master)](https://coveralls.io/github/mimesis-lab/mimesis-factory?branch=master)\n[![PyPI version](https://badge.fury.io/py/mimesis-factory.svg)](https://badge.fury.io/py/mimesis-factory) [![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n\n<a href="https://github.com/mimesis-lab/mimesis-factory">\n    <p align="center">\n        <img src="https://raw.githubusercontent.com/mimesis-lab/mimesis-factory/master/media/logo.png?raw=true">\n    </p>\n</a>\n\n\n## Description\n\n[Mimesis](https://github.com/lk-geimfari/mimesis) integration for [`factory_boy`](https://github.com/FactoryBoy/factory_boy).\n\n## Installation\n\n```python\n➜  pip install mimesis_factory\n```\n\n\n## Usage\n\nLook at the example below and you’ll understand how it works:\n\n```python\nclass Account(object):\n    def __init__(self, username, email, name, surname, age):\n        self.username = username\n        self.email = email\n        self.name = name\n        self.surname = surname\n        self.age = age\n```\n\nNow, use the `MimesisField` class from `mimesis_factory`\nto define how fake data is generated:\n\n```python\nimport factory\nfrom mimesis_factory import MimesisField\n\nfrom account import Account\n\n\nclass AccountFactory(factory.Factory):\n    class Meta(object):\n        model = Account\n\n    username = MimesisField(\'username\', template=\'l_d\')\n    name = MimesisField(\'name\', gender=\'female\')\n    surname = MimesisField(\'surname\', gender=\'female\')\n    age = MimesisField(\'age\', minimum=18, maximum=90)\n    email = factory.LazyAttribute(\n        lambda instance: \'{0}@example.org\'.format(instance.username)\n    )\n    access_token = MimesisField(\'token\', entropy=32)\n```\n\n\n## pytest\n\nWe also recommend to use [`pytest-factoryboy`](https://github.com/pytest-dev/pytest-factoryboy).\nThis way it will be possible to integrate your factories into `pytest` fixtures.\n\n\n## License\n\n`mimesis_factory` is released under the MIT License.\n',
    'author': 'Nikita Sobolev',
    'author_email': 'mail@sobolevn.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mimesis-lab/mimesis-factory',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
