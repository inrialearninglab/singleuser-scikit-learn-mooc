from setuptools import setup, find_packages

try:
    long_desc = open('README.md').read()
except:
    long_desc = ''

setup(
    name="nbreset",
    url="https://github.com/brospars/nbreset",
    author="Benoit Rospars",
    author_email="benoit.rospars@inria.fr",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "jupyter==1"
    ],
    include_package_data=True,
    description="Add reset button in menu",
    long_description=long_desc,
)