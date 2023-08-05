import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arun_test_package_1961", # Replace with your own username
    version="0.0.1",
    author="Zana",
    author_email="aarunkaashyap@gmail.com",
    description="A small example package to test backend functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcarun123/air_backend_test",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
