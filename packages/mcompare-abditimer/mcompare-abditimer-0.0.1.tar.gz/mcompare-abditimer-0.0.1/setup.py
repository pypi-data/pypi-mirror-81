import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcompare-abditimer", 
    version="0.0.1",
    author="Abdi Timer",
    author_email="thatimer@gmail.com",
    description="Wrapper for SKLearn Models",
    long_description='', # TODO
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject", # add github link
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)