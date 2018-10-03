import setuptools
from sintak_parser.utils.core import settings

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sinunika_parser",
    version=settings.VERSION,
    author="lintangtimur",
    author_email=settings.DEV_EMAIL_ADDRESS,
    description=settings.DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lintangtimur/SintakParser",
    packages=['sinunika_parser'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)