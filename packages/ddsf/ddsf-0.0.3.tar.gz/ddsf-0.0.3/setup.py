from setuptools import setup, find_packages

setup(
    name='ddsf',
    description='access dsf',
    version='0.0.3',
    author='Lukas Jurk',
    author_email='lukas.jurk@tu-dresden.de',
    url='https://gitlab.hrz.tu-chemnitz.de/slm/python-ddsf',
    packages=find_packages(),
    install_requires=[
        "requests",
        "requests_ntlm",
    ],
)
