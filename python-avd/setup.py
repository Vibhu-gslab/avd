# from .version import VERSION
import setuptools

setuptools.setup(
    name="pyavd",
    # version=VERSION,
    copyright="Copyright 2023 Arista Networks",
    license = "Apache 2.0",
    author="Arista Networks",
    author_email="",
    description="Arista validated designs",
    #long_description= open('README.md').read(),
    packages=setuptools.find_packages(),
    include_package_data=True,
    #install_requires=[],
    classifiers=[
        'Programming Language :: Python 3.10',
    ],
    entry_points={
        'console_scripts': [
            'pyavd_runner=pyavd:runner1',
        ]
    }
)
