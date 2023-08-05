from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='jojo-hsg',
    version=0.1,
    description='Welcome Stand Users',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["hello", "dio", "jotaro", "joseph"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    install_requires=[
        "setuptools >= 45.2.0"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    url="https://github.com/harisriguhan-facetagr/jojo",
    author="Harisriguhan Sivakumar",
    author_email="harisriguhan.s@facetagr.com",
    license="LICENSE.txt",
)
