import setuptools
from ultimaker import __version__

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="ultimaker-printer-api",
    version=__version__,
    author="Sameer Puri",
    author_email="purisame@spuri.io",
    description="An Ultimaker Printer API client implementation in Python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/vanderbilt-design-studio/python-ultimaker-printer-api",
    packages=setuptools.find_packages(),
    test_suite='test',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "zeroconf",
        "requests",
        "uuid",
    ],
)
