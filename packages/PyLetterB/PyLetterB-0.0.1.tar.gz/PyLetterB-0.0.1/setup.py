import setuptools

setuptools.setup(
    name="PyLetterB",
    version="0.0.1",
    author="Michael Andersen",
    author_email="mjpandersen@gmail.com",
    description="An unoffical letterboxd API for user likes",
    long_description="An unoffical letterboxd API for user likes",
    long_description_content_type="text/markdown",
    url="https://github.com/Michael-Andersen/PyLB",
    packages=setuptools.find_packages(),
    install_requires=['beautifulsoup4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
