from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='weighted_kdtree',
      packages=['weighted_kdtree'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Monisha Siddananda Sampaths',
      author_email='monisam97@gmail.com',
      url='https://github.com/moni97/kdtreePython',
      version='0.1.1',
      )