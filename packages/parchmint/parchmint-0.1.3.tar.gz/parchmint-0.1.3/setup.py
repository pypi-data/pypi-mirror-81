# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parchmint']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0']

setup_kwargs = {
    'name': 'parchmint',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Radhakrishna Sanka',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
