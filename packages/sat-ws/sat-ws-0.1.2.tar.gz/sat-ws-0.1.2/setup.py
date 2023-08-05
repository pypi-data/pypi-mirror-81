import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sat-ws",
    version="0.1.2",
    author="Moisés Navarro",
    author_email="moisalejandro@gmail.com",
    description="API to connect with SAT ws",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/HomebrewSoft/sat_ws_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
