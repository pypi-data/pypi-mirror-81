# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_commit_poetry_export']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['poetry-export = '
                     'pre_commit_poetry_export.poetry_export:main']}

setup_kwargs = {
    'name': 'pre-commit-poetry-export',
    'version': '0.1.1',
    'description': 'pre-commit hook to keep requirements.txt updated',
    'long_description': '# pre-commit-poetry-export\nPre-commit hook to keep requirements.txt updated\n',
    'author': 'Antonio Luckwu',
    'author_email': 'victor.luckwu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/avlm/pre-commit-poetry-export',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
