from distutils.core import setup

setup(
    name='dectools',
    version='0.1.1',
    author='Charles Merriam',
    author_email='charles.merriam@gmail.com',
    packages=['dectools', 'dectools.test'],
    url='http://pypi.python.org/pypi/dectools/',
    license='LICENSE.txt',
    description='Decorator toolkit library',
    long_description=open('README.txt').read(),
)

