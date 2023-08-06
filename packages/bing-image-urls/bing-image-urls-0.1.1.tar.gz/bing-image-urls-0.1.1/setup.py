# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bing_image_urls']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.15.5,<0.16.0', 'logzero>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'bing-image-urls',
    'version': '0.1.1',
    'description': 'fetch bing image urls based on keywords',
    'long_description': '# Bing-Image-Urls ![build](https://github.com/ffreemt/bing-image-urls/workflows/build/badge.svg)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/bing-image-urls.svg)](https://badge.fury.io/py/bing-image-urls)\n\nFetch Bing image urls based on keywords\n\n### Installation\n```pip install bing-image-urls```\n\n### Usage\n\n```python\n\nfrom bing_image_urls import bing_image_urls\n\nprint(bing_iamge_urls("bear", limit=2))\n# [\'https://www.stgeorgeutah.com/wp-content/uploads/2017/01/blackbear.jpg\',\n# \'http://www.cariboutrailoutfitters.com/wp-content/uploads/2017/03/saskatchewan-black-bear-hunting.jpg\']\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/light-aligner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
