import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='json-fingerprint',
    version='0.0.3',
    author='Ville Lehtinen',
    author_email='ville.lehtinen@cobaltine.fi',
    license='MIT',
    description='json fingerprinting tool for creating consistent and comparable checksums of unordered json data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cobaltine/json-fingerprint',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
