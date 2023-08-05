# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twopic']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.2.1,<3.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'nltk>=3.5,<4.0',
 'pandas>=1.1.2,<2.0.0',
 'tensorflow>=2.3.1,<3.0.0',
 'tensorflow_hub>=0.9.0,<0.10.0',
 'tqdm>=4.50.0,<5.0.0',
 'twittenizer>=0.0.5,<0.0.6']

setup_kwargs = {
    'name': 'twopic',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Kydlaw',
    'author_email': 'kydlawj@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
