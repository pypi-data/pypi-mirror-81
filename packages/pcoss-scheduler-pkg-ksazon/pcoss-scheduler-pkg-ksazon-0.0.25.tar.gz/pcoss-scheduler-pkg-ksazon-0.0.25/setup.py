import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="pcoss-scheduler-pkg-ksazon",
    version="0.0.25",
    author="Krzysztof Sazon",
    author_email="krzysztof.sazon@gmail.com",
    description="Tabular data PCOSS calculations module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ksazon/mgr/mgr_client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=required
)
