from setuptools import setup

requires = [
    'ipython',
    'Quandl',
    'pandas',
    'requests',
    'yelp',
    'ipdb',
    'python-google-places',
]

setup(
    name='server',
    install_requires=requires
)
