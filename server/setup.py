from setuptools import setup


setup(
    name='restoweb',
    packages=['restoweb'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'autopep8',
        'pre-commit'
    ],
)
