import setuptools
import os

# Get requirements
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robustneldermead",
    version="1.4",
    author="Bryson Cale",
    author_email="bryson.cale1@gmail.com",
    description="Nelder Mead algorithm for high dimensional parameter spaces",
    longdescription=long_description,
    long_description_content_type="text/x-rst",
    packages = setuptools.find_packages(),
    data_files = [("", ["LICENSE.txt"])],
    include_package_data=True,
    install_requires=install_requires,
    url="https://github.com/astrobc1/neldermead",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix"
    ],
    python_requires='>=3.6'
)