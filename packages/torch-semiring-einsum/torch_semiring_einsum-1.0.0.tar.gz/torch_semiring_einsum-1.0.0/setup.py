# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_semiring_einsum']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'torch-semiring-einsum',
    'version': '1.0.0',
    'description': 'Extensible PyTorch implementation of einsum that supports multiple semirings',
    'long_description': None,
    'author': 'Brian DuSell',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bdusell.github.io/semiring-einsum/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
