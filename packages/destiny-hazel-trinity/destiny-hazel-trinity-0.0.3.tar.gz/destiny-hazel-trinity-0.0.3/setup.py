from setuptools import setup, find_packages

import destiny

setup(
    name='destiny-hazel-trinity',
    version=destiny.VERSION,
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.6.2',
        'aiosqlite>=0.11.0',
        'async_timeout>=3.0.1'
    ],
    author='Hazel Trinity',
    python_requires='>=3.6'
)
