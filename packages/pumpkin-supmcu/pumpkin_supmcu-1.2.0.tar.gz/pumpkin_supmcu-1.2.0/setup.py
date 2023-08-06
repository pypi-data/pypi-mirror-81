# pylint: skip-file
import os
import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A library to interface with Pumpkin SupMCU modules via I2C."

try:
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
        requirements = requirements.splitlines()
        requirements = [r for r in requirements if r.strip() != '']
except FileNotFoundError:
    # User installing from pip
    requirements = [
        'pyserial'
    ]

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    version = '1.2.0'  # Makes sure the read the docs version can build.

setuptools.setup(
    name="pumpkin_supmcu",
    version=version,
    author="James Womack",
    author_email="info@pumpkininc.com",
    description="A library to interface with Pumpkin SupMCU modules via I2C",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pumpkin-space-systems/public/pumpkin-supmcu",
    packages=['pumpkin_supmcu.i2c', 'pumpkin_supmcu.supmcu'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.7',
    zip_safe=False
)
