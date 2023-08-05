import setuptools
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setuptools.setup(
    name="mcompare", 
    version="1.0.0",
    author="Abdi Timer",
    author_email="thatimer@gmail.com",
    description="Wrapper for SKLearn Models",
    long_description=README, 
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/abditimer/mcompare", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)