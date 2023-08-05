import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pykkachu",
    version="0.0.1",
    author="Andrew McKnight",
    author_email="thedonk@gmail.com",
    description="An Actor Model which packages Pykka and FSMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amcknight/pykkachu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
