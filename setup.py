"""Setup script for SixSpec."""

from setuptools import setup, find_packages

setup(
    name="sixspec",
    version="0.1.0",
    description="Dimensional specification framework with W5H1 objects",
    author="SixSpec Contributors",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
        ]
    },
    package_data={
        'sixspec.git.hooks': ['commit-msg'],
    },
    entry_points={
        'console_scripts': [
            # Future: 'sixspec=sixspec.cli:main',
        ],
    },
)