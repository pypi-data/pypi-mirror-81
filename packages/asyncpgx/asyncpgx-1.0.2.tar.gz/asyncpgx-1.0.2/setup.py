# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncpgx', 'asyncpgx.tests']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'asyncpgx',
    'version': '1.0.2',
    'description': '',
    'long_description': None,
    'author': 'Vladislav Laukhin',
    'author_email': 'laukhin97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
