# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncpixel', 'asyncpixel.exceptions', 'asyncpixel.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'asyncpixel',
    'version': '0.2.0',
    'description': 'An async wrapper for hypixel',
    'long_description': '# AsyncPixel\n\n## Asynchronous Hypixel API Wrapper\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8a67753c7c684a5ca8cff399006f22d7)](https://www.codacy.com/gh/Obsidion-dev/asyncpixel?utm_source=github.com&utm_medium=referral&utm_content=Obsidion-dev/asyncpixel&utm_campaign=Badge_Grade)\n[![Our Support Server](https://discordapp.com/api/guilds/695008516590534758/widget.png?style=shield)](https://discord.gg/invite/7BRD7s6)\n[![Support us on Patreon](https://img.shields.io/badge/Support-us!-yellow.svg)](https://www.patreon.com/obsidion) [![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Tests](https://github.com/Obsidion-dev/asyncpixel/workflows/Tests/badge.svg)](https://github.com/Obsidion-dev/asyncpixel/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/Obsidion-dev/asyncpixel/branch/master/graph/badge.svg)](https://codecov.io/gh/Obsidion-dev/asyncpixel)\n[![PyPI](https://img.shields.io/pypi/v/asyncpixel.svg)](https://pypi.org/project/asyncpixel/)\n[![Read the Docs](https://readthedocs.org/projects/asyncpixel/badge/)](https://asyncpixel.readthedocs.io/)\n\n### Overview\n\nThis is an asynchronous python wrapper for the [hypixel api](https://api.hypixel.net). It is available for download on [pypi](https://pypi.org/project/asyncpixel/)\n\n### Endpoints\n\n## Examples\n\n### Basic use\n\n```python\nimport asyncpixel\nimport asyncio\n\nuuid = "405dcf08b80f4e23b97d943ad93d14fd"\n\n\nasync def main():\n    client = asyncpixel.Client("hypixel_api_key")\n    print(await client.get_profile("405dcf08b80f4e23b97d943ad93d14fd"))\n    await client.close()\n\n\nasyncio.run(main())\n```\n',
    'author': 'Darkflame72',
    'author_email': 'leon@bowie-co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Obsidion-dev/asyncpixel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
