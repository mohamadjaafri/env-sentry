from setuptools import find_packages, setup

setup(
    name="env-sentry",
    version="0.2.0",
    packages=find_packages(exclude=("tests",)),
    install_requires=["click>=8.1,<9", "rich>=13,<15"],
    extras_require={
        "dev": [
            "pytest>=8,<9",
            "pytest-cov>=5,<7",
            "ruff>=0.6,<1",
        ]
    },
    entry_points={"console_scripts": ["env-sentry=envsentry.cli:scan"]},
    author="Mohamad Al Jaafri",
    description="A redacting CLI scanner for possible secrets in dotenv files",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
