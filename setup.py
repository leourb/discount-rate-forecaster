import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ggm_calculator",
    version="1.0.0",
    author="Leonardo Urbano",
    author_email="leonardo.urbano87@libero.it",
    packages=setuptools.find_packages(),
    description="Gordon Growth Model Calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/leourb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
