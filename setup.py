from setuptools import setup, find_packages

setup(name='interactive_learning',
      version='0.0.1',
      author='Brandyn A. White',
      packages=find_packages(),
      package_data={'interactive_learning.image_selector': ['*.html']},
      author_email='bwhite@dappervision.com',
      license='GPLv3')
