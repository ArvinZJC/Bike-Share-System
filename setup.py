# TODO: still under construction; do not run this file!
from setuptools import setup, find_packages

setup(
    name = 'BikeSims',
    version = '2.0.0',
    author = 'test1',
    description = 'test',
    license = 'GPLv3',
    keywords = 'test',
    url = 'https://github.com/ArvinZJC/Bike-Share-System',  # TODO: change to GitLab
    packages = find_packages(),
    include_package_data = True,
    # TODO: data_files = ,
    # TODO: platforms = 'any',
    install_requires = [
        'matplotlib==3.3.4',
        'numpy==1.20.1',
        'pandas==1.2.2',
        'Pillow==8.1.0'
    ],
    entry_points={'console_scripts': [
        'bss_run = bss.main:main'
    ]},
    zip_safe = False
)