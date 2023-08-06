from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    readme_as_long_description = f.read()

setup(
    name="nemf",
    version="0.3.4",
    packages=find_packages(),

    # install_requires=[""],

    # metadata to display on PyPI
    author="Laurin Steidle",
    author_email="laurin.steidle@uni-hamburg.de",
    description="Network-based ecosystem Modelling Framework",
    long_description=readme_as_long_description,
    long_description_content_type="text/markdown",
    keywords="ecosystem modelling framework inverse-modelling",
    url="https://github.com/465b/nemf/",
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha',
    ],
    license='BSD',
    install_requires=[
        'numpy','seaborn','pandas','matplotlib','networkx','pyyaml', 
        'termcolor']
)