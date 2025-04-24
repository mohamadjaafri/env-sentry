from setuptools import setup, find_packages

setup(
    name='env-sentry',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'env-sentry=envsentry.cli:scan',
        ],
    },
    author='Mohamad Al Jaafri',
    description='CLI tool to scan .env files for secrets',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
