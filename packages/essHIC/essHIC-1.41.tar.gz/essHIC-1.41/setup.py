from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'pipREADME.md')) as f:
    long_description = f.read()

setup(name='essHIC',
      version='1.41',
      description='essHIC is a python module to compare HiC matrices by computing a metric distance between them',
      url='https://github.com/stefanofranzini/essHIC',
      author='Stefano Franzini',
      author_email='sfranzin@sissa.it',
      license='MIT',
      packages=['essHIC'],
  install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'sklearn'
      ],
      zip_safe=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['HiC','distance','spectral'])
