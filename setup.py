from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="soltxs",
    version="1.0.8",
    author="Quick Vectors",
    author_email="felipe@qvecs.com",
    description="Solana transaction normalizer, parser, and resolver.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/qvecs/soltxs",
    project_urls={
        "Bug Tracker": "https://github.com/qvecs/soltxs/issues",
        "Source Code": "https://github.com/qvecs/soltxs",
    },
    python_requires=">=3.10",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    install_requires=[
        "qborsh==1.0.1",
        "qbase58==1.0.4",
    ],
    extras_require={"dev": ["pytest"]},
)
