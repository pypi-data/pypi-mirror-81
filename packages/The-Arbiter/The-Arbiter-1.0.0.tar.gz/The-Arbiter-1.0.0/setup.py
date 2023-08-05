import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="The-Arbiter",
    version="1.0.0",
    author="Cole Kelley",
    author_email="ck@codejuicer.com",
    license="MIT",
    description="An argument validation library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/codejuicer/the-arbiter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    PROJECT_URLS = {
        "Source Code": "https://gitlab.com/codejuicer/the-arbiter",
    },
    python_requires='>=3',
    keywords=['validation', 'arguments']
)
