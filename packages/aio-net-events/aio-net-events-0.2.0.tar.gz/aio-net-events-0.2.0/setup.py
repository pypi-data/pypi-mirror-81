# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aio_net_events', 'aio_net_events.backends']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=2.0.2,<3.0.0', 'netifaces>=0.10.9,<0.11.0']

extras_require = \
{':sys_platform == "darwin"': ['pyobjc-core>=6.2.2,<7.0.0',
                               'pyobjc-framework-Cocoa>=6.2.2,<7.0.0',
                               'pyobjc-framework-SystemConfiguration>=6.2.2,<7.0.0']}

setup_kwargs = {
    'name': 'aio-net-events',
    'version': '0.2.0',
    'description': 'Asynchronous network configuration event detector for Python 3.6 and above',
    'long_description': '# aio-net-events\n\n`aio-net-events` is a Python library that provides asynchronous generators\nyielding events when the network configuration of the machine changes.\nCurrently only network interface additions / removals and IP address additions /\nremovals are supported; more events may be added later.\n\nSupports Windows, Linux and macOS at the moment.\n\nRequires Python >= 3.5.\n\nWorks with [`asyncio`](https://docs.python.org/3/library/asyncio.html),\n[`curio`](https://curio.readthedocs.io/en/latest/) and\n[`trio`](https://trio.readthedocs.io/en/stable/).\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install\n`aio-net-events`.\n\n```bash\npip install aio-net-events\n```\n\n## Usage\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to\ndiscuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Tamas Nepusz',
    'author_email': 'tamas@collmot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ntamas/aio-net-events/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
