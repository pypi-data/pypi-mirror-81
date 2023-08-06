import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='seqalign',
    version='0.0.3',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='Manage sequence alignments',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/seqalign.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['biopython', 'pyhg19', 'tempfifo'],
    entry_points={
        # 'console_scripts': []
    }
)
