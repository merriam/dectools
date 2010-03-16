from distutils.core import setup

setup(
    name='dectools',
    version='0.1.4',
    author='Charles Merriam',
    author_email='charles.merriam@gmail.com',
    packages=['dectools', 'dectools.test'],
    url='http://charlesmerriam.com/dectools/',
    license='MIT License',
    description='decorator toolkit library',
    long_description=open('README.txt').read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Natural Language :: English',
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        ],
    requires=['decorator (>=3.1)'],
)


