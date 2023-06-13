from setuptools import setup
from setuptools import find_packages

setup(
    name='binance-liquidation-feeder',
    version="1.0.0",
    description='Notify liquidation on Binance.',
    install_requires=[],
    author='aoki-h-jp',
    author_email='aoki.hirotaka.biz@gmail.com',
    license='MIT',
    packages=find_packages(
        include=['feeder'],
        exclude=['img']
    ),
)
