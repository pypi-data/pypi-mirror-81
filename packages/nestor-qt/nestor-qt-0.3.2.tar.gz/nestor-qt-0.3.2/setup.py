# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nestor_qt',
 'nestor_qt.resources',
 'nestor_qt.store_data',
 'nestor_qt.store_data.objects']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.4,<4.0.0',
 'nist-nestor>=0.4.3,<0.5.0',
 'pyaml>=20.4.0,<21.0.0',
 'pyqt5>=5.15.0,<6.0.0',
 'seaborn>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['nestor-qt = nestor_qt.app:main']}

setup_kwargs = {
    'name': 'nestor-qt',
    'version': '0.3.2',
    'description': 'Legacy (Qt5) GUI for the Nestor annotation tool',
    'long_description': None,
    'author': 'tbsexton',
    'author_email': 'thurston.sexton@nist.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.nist.gov/services-resources/software/nestor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
