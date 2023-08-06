import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="auto-caption",
    version="0.0.6",
    author="Guangrui Wang",
    author_email="aguang.xyz@gmail.com",
    description="Automatic captioning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aguang-xyz/auto-caption",
    packages=setuptools.find_packages(),
    scripts=["bin/auto-caption"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>= 3.6',
    install_requires=[
        'moviepy',
        'pydub',
        'vosk',
        'tqdm',
        'nnsplit'
    ])
