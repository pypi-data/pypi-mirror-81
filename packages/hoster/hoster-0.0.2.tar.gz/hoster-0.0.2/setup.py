from setuptools import setup
with open("README.rst", "r") as fh:
    long_description = fh.read()
setup(
    name='hoster',
    version='0.0.2',
    description='hoster is a python module that hosts code',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['hoster'],
    author='henos',
    author_email='henos1029@gmail.com',
    keywords=['alive', 'keep alive', 'henos', 'host', 'hoster'],
    url='https://github.com/henos1029/hoster'
)