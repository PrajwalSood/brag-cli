from setuptools import setup, find_packages

setup(
    name="brag-cli",
    version="0.1.0",
    description="A CLI tool to create and manage a brag document, sync with git, and generate summaries and resume bullet points using Ollama.",
    author="Prajwal Sood",
    packages=find_packages(),
    install_requires=[
        "typer",
        "GitPython",
        "requests",
        "pydantic"
    ],
    entry_points={
        "console_scripts": [
            "brag=brag.cli:app"
        ]
    },
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 