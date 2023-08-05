# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caldera',
 'caldera._setup',
 'caldera.blocks',
 'caldera.data',
 'caldera.data.utils',
 'caldera.dataset',
 'caldera.models',
 'caldera.testing',
 'caldera.transforms',
 'caldera.transforms.networkx',
 'caldera.utils',
 'caldera.utils.functional',
 'caldera.utils.mp',
 'caldera.utils.nx',
 'caldera.utils.nx.generators',
 'caldera.utils.nx.traversal']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.2.0,<21.0.0',
 'colorama>=0.4.3,<0.5.0',
 'dill>=0.3.2,<0.4.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.18.4,<2.0.0',
 'pytest-randomly>=3.4.1,<4.0.0',
 'scipy>=1.5.2,<2.0.0',
 'torch-scatter>=2.0.4,<3.0.0',
 'torch>=1.5.0,<2.0.0']

extras_require = \
{'docs': ['sphinx_autodoc_typehints>=1.11.0,<2.0.0',
          'sphinx>=3.2.1,<4.0.0',
          'keats>=0.2.28,<0.3.0',
          'sphinx_bootstrap_theme>=0.7.1,<0.8.0',
          'nbformat>=5.0.7,<6.0.0',
          'nbconvert>=5.6.1,<6.0.0',
          'jupyter-sphinx>=0.3.1,<0.4.0'],
 'lint': ['pytest-cov>=2.10.0,<3.0.0',
          'black>=19.10b0,<20.0',
          'pre-commit>=2.6.0,<3.0.0',
          'pylint>=2.5.3,<3.0.0'],
 'nbexamples': ['seaborn>=0.11.0,<0.12.0',
                'matplotlib>=3.3.1,<4.0.0',
                'tqdm>=4.48.2,<5.0.0',
                'pytorch-lightning>=0.9.0,<0.10.0',
                'hydra-core>=1.0.0,<2.0.0',
                'rich>=7.0.0,<8.0.0',
                'h5py>=2.10.0,<3.0.0'],
 'xtests': ['pytest-sugar>=0.9.4,<0.10.0']}

setup_kwargs = {
    'name': 'pytorch-caldera',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.github.com/jvrana/caldera',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
