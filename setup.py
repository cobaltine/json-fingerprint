import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open(".version", "r", encoding="utf-8") as f:
    version_raw = f.read()[1:]  # omit 'v'
    version = version_raw.split("-")[0]  # omit trailing version identifiers

setuptools.setup(
    name="json-fingerprint",
    version=version,
    author="Ville Lehtinen",
    author_email="ville.lehtinen@cobaltine.fi",
    license="MIT",
    description="Create consistent and comparable fingerprints with secure hashes from unordered JSON data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cobaltine/json-fingerprint",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
