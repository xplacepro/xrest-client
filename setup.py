import os
from setuptools import setup

BASE_PATH = os.path.dirname(__file__)

with open(os.path.join(BASE_PATH, 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(BASE_PATH, 'requirements.txt')) as readme:
    requirements = readme.read()

with open(os.path.join(BASE_PATH, 'test_requirements.txt')) as readme:
    test_requirements = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='xrest_client',
    version='0.1',
    packages=['xrest_client'],
    install_requires=requirements,
    tests_require=test_requirements,
    include_package_data=True,
    license='BSD License',
    description='A simple client for XRest.',
    long_description=README,
    url='https://github.com/xplacepro/xrest-client.git',
    author='Alex Sofin',
    author_email='sofin.moffin@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)