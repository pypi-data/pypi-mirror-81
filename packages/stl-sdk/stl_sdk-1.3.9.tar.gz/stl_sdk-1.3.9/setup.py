from setuptools import setup, find_packages
from codecs import open
from os import path

from stl_sdk import VERSION

__version__ = VERSION

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='stl_sdk',
    version=__version__,
    description='Spacetime Python SDK',
    long_description=long_description,
    url='https://github.com/spacetimelabs/stl_sdk',
    download_url='https://github.com/spacetimelabs/stl_sdk/tarball/' + __version__,
    author='Spacetime Labs',
    author_email='lc@spacetimelabs.ai',
    license='BSD',
    keywords='',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    package_dir={'stl_sdk': 'stl_sdk'},
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    zip_safe=False
)
