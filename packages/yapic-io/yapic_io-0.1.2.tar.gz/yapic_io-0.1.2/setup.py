import os

from setuptools import setup

reqs = ['numpy>=1.13.1',
        'munkres>=1.0.8',
        'scikit_image>=0.12.3',
        'pyilastik>=0.0.7',
        'bigtiff>=0.1.2']


def readme():
    README_rst = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(README_rst) as f:
        return f.read()


setup(name='yapic_io',
      version='0.1.2',
      description='io data handling module for various image sources as interface for pixel classification tools',
      long_description=readme(),
      author='Manuel Schoelling, Christoph Moehl',
      author_email='manuel.schoelling@dzne.de, christoph.moehl@dzne.de',
      packages=['yapic_io'],
      zip_safe=False,
      install_requires=reqs,
      test_suite='nose.collector',
      tests_require=['coverage', 'nose-timer', 'nose'])
