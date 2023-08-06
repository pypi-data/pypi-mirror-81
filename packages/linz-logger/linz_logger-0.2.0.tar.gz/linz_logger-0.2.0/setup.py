# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linz_logger']

package_data = \
{'': ['*']}

install_requires = \
['structlog>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'linz-logger',
    'version': '0.2.0',
    'description': 'LINZ standard Logging format',
    'long_description': '\n# Python LINZ Logger\n[![GitHub Actions Status](https://github.com/linz/python-linz-logger/workflows/Build/badge.svg)](https://github.com/linz/python-linz-logger/actions)\n[![Kodiak](https://badgen.net/badge/Kodiak/enabled?labelColor=2e3a44&color=F39938)](https://kodiakhq.com/)\n[![Dependabot Status](https://badgen.net/badge/Dependabot/enabled?labelColor=2e3a44&color=blue)](https://github.com/linz/python-linz-logger/network/updates)\n[![License](https://badgen.net/github/license/linz/python-linz-logger?labelColor=2e3a44&label=License)](https://github.com/linz/python-linz-logger/blob/master/LICENSE)\n[![Conventional Commits](https://badgen.net/badge/Commits/conventional?labelColor=2e3a44&color=EC5772)](https://conventionalcommits.org)\n[![Code Style](https://badgen.net/badge/Code%20Style/black?labelColor=2e3a44&color=000000)](https://github.com/psf/black)\n\n## Why?\n\nLINZ has a standard Logging format based loosly on [pinojs](https://github.com/pinojs/pino) logging format \n\n```json\n{\n    "level": 30,\n    "time": 1571696532994,\n    "pid": 10671,\n    "hostname": "Ubuntu1",\n    "id": "01DQR6KQG0K60TP4T1C4VC5P74",\n    "msg": "SomeMessage",\n    "v": 1\n}\n```\n\n## Usage \n\n```\npip install linz.logger\n```\n\n\n```python\nfrom linz.logger import get_log\n\n\nget_log().info("Hello World")\n```',
    'author': 'Blayne',
    'author_email': 'bchard@linz.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linz/python-linz-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
