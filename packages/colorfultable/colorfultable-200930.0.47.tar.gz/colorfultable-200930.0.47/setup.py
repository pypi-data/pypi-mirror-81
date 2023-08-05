import os

from setuptools import find_packages, setup

from colorfultable import author, author_email, name, version, website1

description = 'A module to help print beautiful table on the terminal.'
long_description = description

if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as mdfile:
        long_description = mdfile.read()

install_requires = ['colorama>=0.4.3'] if os.name == 'nt' else None

setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    packages=find_packages(),
    platforms='any',
    url=website1,
    python_requires='>=3.5',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords=['table', 'console', 'terminal', 'colorful', 'text'],
)
