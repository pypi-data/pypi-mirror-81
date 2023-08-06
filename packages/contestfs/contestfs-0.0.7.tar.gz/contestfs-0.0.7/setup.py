# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['contestfs']
install_requires = \
['colorama>=0.4.3,<0.5.0', 'watchdog>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['contestfs = contestfs:main']}

setup_kwargs = {
    'name': 'contestfs',
    'version': '0.0.7',
    'description': 'continuously test file system changes, and run a command.',
    'long_description': '# Usage\n\n```\ncontestfs <extensions-to-watch> <command-on-change>\n```\n\nexmaple:\n\n```\ncontestfs py python -m unittest\n```\n\n```\ncontestfs py,pyi mypy --ignore-missing-import .\n```\n',
    'author': 'Jeong-Min Lee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
