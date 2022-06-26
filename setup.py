from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "solute",
    version = "3.0",
    description = "hide text inside an image. additional text encryption inbuilt",
    url = "https://github.com/SathvikPN/Solute",
    author = "Sathvik PN",
    packages = ["solute"],
    install_requires = required,
)