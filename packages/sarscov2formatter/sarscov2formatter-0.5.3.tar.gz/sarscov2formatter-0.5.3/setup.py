import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sarscov2formatter",
    version="0.5.3",
    author="Nick Keener",
    author_email="nickeener@gmail.com",
    description="Formats metadata and MSA for Galaxy SARS-CoV2 Selection Analysis workflow",
    install_requires=['biopython'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nickeener/sarscov2formatter",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['sarscov2formatter=sarscov2formatter.cli:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Academic Free License (AFL)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

