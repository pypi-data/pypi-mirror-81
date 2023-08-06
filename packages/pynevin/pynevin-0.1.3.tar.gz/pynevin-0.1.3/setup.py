import pathlib
from setuptools import setup, find_packages
from pynevin.pypi import get_latest_version

HERE = pathlib.Path(__file__).parent

VERSION = get_latest_version()
PACKAGE_NAME = 'pynevin'
AUTHOR = 'Nevin'
AUTHOR_EMAIL = 'pynevin@idarkduck.com'
URL = 'https://github.com/iDuckDark/PyNevin'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Describe your package in one sentence'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )