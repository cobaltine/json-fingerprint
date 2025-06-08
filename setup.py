import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open(".version", "r", encoding="utf-8") as f:
    version_raw = f.read()[1:]  # omit "v"
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
    keywords="json fingerprint hash",
    project_urls={
        "Changelog": "https://github.com/cobaltine/json-fingerprint/releases",
        "Homepage": "https://github.com/cobaltine/json-fingerprint",
        "Source": "https://github.com/cobaltine/json-fingerprint",
        "Tracker": "https://github.com/cobaltine/json-fingerprint/issues",
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Topic :: File Formats :: JSON",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
)
