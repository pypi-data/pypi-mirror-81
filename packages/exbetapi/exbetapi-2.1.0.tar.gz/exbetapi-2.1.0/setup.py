# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exbetapi']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.4.1,<6.0.0', 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'exbetapi',
    'version': '2.1.0',
    'description': 'Python Bindings for Trading API for exbet.io',
    'long_description': None,
    'author': 'Python Development Team',
    'author_email': 'py@exbet.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exbet/python-exbetapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
