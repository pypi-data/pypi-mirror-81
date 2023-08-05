from setuptools import setup, find_packages

setup(
   name='SoundsLike',
   version='0.0.11',
   author='Tal Zaken',
   author_email='talzaken@gmail.com',
   packages=find_packages(),
   #scripts=['bin/script1','bin/script2'],
   url='http://github.com/tal-z/SoundsLike/',
   license='LICENSE',
   description='SoundsLike is a python package that helps find words that sound like other words.',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "cmudict >= 0.4.4",
       "g2p-en >= 2.1.0",
   ],
)