import setuptools

setuptools.setup(
    name='compound_split',
    version='0.1.0.dev2',
    install_requires=[],
    python_requires='>=3',
    author="Don Tuggener",
    author_email="don.tuggener@gmail.com",
    description="Splits a German compound into its body and head",
    license='GPL-3.0 License',
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JoelNiklaus/CharSplit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
