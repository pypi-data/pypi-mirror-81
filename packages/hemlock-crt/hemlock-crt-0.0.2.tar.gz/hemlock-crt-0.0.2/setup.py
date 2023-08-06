import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hemlock-crt",
    version="0.0.2",
    author="Dillon Bowen",
    author_email="dsbowen@example.com",
    description="Cognitive Reflection Test for Hemlock projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsbowen/hemlock-crt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)