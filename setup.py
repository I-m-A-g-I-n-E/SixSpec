"""Setup script for SixSpec."""

from setuptools import setup, find_packages

setup(
    name="sixspec",
    version="0.1.0",
    description="Dimensional specification framework with Chunk objects",
    author="SixSpec Contributors",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        'networkx>=3.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
        ],
        # Claude Agent SDK integration for session management and pause/resume
        'claude': [
            'claude-agent-sdk>=0.1.0',
        ],
        # DEPRECATED: A2A integration (use 'claude' extra instead)
        'a2a': [
            # DEPRECATED: Use ClaudeWalker with 'claude' extra instead
            # See MIGRATION_A2A_TO_CLAUDE_SDK.md for migration guide
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