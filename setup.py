"""Setup script for SixSpec."""

from setuptools import setup, find_packages

setup(
    name="sixspec",
    version="0.1.0",
    description="Dimensional specification framework with Chunk objects",
    author="SixSpec Contributors",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
        ],
        # A2A integration for production-ready task lifecycle
        # Note: Google's A2A protocol implementation is evolving.
        # Current implementation uses built-in A2A-compatible task management.
        # Future: Add 'agent2agent' and 'grpcio' when officially available.
        'a2a': [
            # 'agent2agent>=0.1.0',  # Future: Google's A2A library
            # 'grpcio>=1.50.0',      # For gRPC streaming
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