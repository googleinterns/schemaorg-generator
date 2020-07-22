import setuptools

setuptools.setup(
    name='schemaorgutils',
    version='0.1.0',
    author='GoogleInc',
    packages=setuptools.find_packages(),
    license='LICENSE.txt',
    description='Utilities that help in generating schemaorg compliant feed.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pyshacl',
        'protobuf',
        'isodate'
    ],
    include_package_data=True
)
