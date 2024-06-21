from setuptools import setup, find_packages

setup(
    name="cooklang-py",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'cooklang=cli.main:cli',
        ],
    },
    description='A pure Python implementation of Cooklang',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/cooklang-py',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
