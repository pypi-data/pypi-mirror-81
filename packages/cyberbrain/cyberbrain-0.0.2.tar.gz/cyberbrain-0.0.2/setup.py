# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyberbrain', 'cyberbrain.generated', 'cyberbrain.internal']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'crayons>=0.3.0,<0.4.0',
 'deepdiff>=5.0.0,<6.0.0',
 'get-port>=0.0.5,<0.0.6',
 'grpcio>=1.30.0,<2.0.0',
 'jsonpickle>=1.4.1,<2.0.0',
 'protobuf>=3.12.2,<4.0.0',
 'pygments>=2.6.1,<3.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'cyberbrain',
    'version': '0.0.2',
    'description': 'Python debugging. Redefined.',
    'long_description': None,
    'author': 'laike9m',
    'author_email': 'laike9m@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
