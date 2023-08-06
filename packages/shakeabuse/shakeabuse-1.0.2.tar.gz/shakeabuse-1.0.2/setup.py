import pathlib
from setuptools import setup
from shakeabuse import __version__


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="shakeabuse",
    version=__version__,
    description="Display a random shakespearean abuse on the console.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/diptangsu/shakeabuse",
    author="Diptangsu Goswami",
    author_email="diptangsu.97@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["shakeabuse"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "shkabuse=shakeabuse.__main__:abuse",
        ]
    },
)
