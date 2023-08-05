import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arris-tg2492lg",
    version="1.0.1",
    author="vanbalken",
    description="Python client for the Arris TG2492LG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanbalken/arris-tg2492lg",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
