try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Logfind',
    'author': 'R Ashwin',
    'url': 'https://github.com/ashwin-5g/logfind',
    'download_url': 'https://github.com/ashwin-5g/logfind',
    'author_email': 'ashwin@5gindia.net',
    'version': '0.1',
    'install_requires': [],
    'packages': ['logfind'],
    'scripts': ['logfind.py'],
    'name': 'logfind'
}

setup(**config)
