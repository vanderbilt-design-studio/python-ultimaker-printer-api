import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ultimaker-printer-api",
    version="0.0.1",
    author="Sameer Puri",
    author_email="purisame@spuri.io",
    description="An Ultimaker Printer API Client implementation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanderbilt-design-studio/python-ultimaker-printer-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
