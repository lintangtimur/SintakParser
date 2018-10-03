import setuptools
from lib.utils.core import settings

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sintak unika parser",
    version=settings.VERSION,
    author="lintangtimur",
    author_email="lintangtimur915@gmail.com",
    description="Packages for parser and scrap information from sintak unika",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lintangtimur/SintakParser",
    packages=['sintak-unika-parser'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)