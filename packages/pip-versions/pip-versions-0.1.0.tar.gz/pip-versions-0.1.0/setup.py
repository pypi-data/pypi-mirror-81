# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pip_versions']

package_data = \
{'': ['*']}

install_requires = \
['cliar>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['pip-versions = pip_versions.cli:entry_point']}

setup_kwargs = {
    'name': 'pip-versions',
    'version': '0.1.0',
    'description': 'Show pip version information from pypi',
    'long_description': 'Installation\n============\n\n.. code-block:: bash\n   :class: ignore\n\n   pip3 install pip-versions\n\n\nUsage\n=====\n\nGet the latest version\n\n.. code-block:: bash\n   :class: ignore\n\n   pip-versions latest django\n\n\n.. code-block:: bash\n   :class: ignore\n\n   3.1.2\n\n\nGet all the versions\n\n.. code-block:: bash\n   :class: ignore\n\n   pip-versions list django\n\n\n.. code-block:: bash\n   :class: ignore\n\n   2.2.15\n   2.2.16\n   3.0\n   3.0.1\n   3.0.2\n   3.0.3\n   3.0.4\n   3.0.5\n   3.0.6\n   3.0.7\n   3.0.8\n   3.0.9\n   3.0.10\n   3.1\n   3.1.1\n   3.1.2\n',
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willemt/pip-versions/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
