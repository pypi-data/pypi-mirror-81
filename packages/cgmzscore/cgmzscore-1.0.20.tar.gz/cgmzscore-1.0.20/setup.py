from setuptools import setup, find_packages

setup(
    name='cgmzscore',
    version='1.0.20',
    license='BSD',


    author='Prajwal Kumar Singh',
    author_email='prajwalsingh651@gmail.com',

    packages=find_packages(),
    include_package_data=True,

    description="z-scores of anthropometric measurements of children below 5 years  based on WHO",
    long_description=open('README').read(),

    classifiers=[
        'Intended Audience :: Healthcare Industry',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: OS Independent',
    ]
)
