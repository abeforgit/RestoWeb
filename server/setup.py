from setuptools import setup


setup(
    name='restoweb',
    packages=['restoweb'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_migrate',
        'flask_bcrypt',
        'flask-cors',
        'flask-testing',
        'autopep8',
        'pre-commit',
        'jinja2',
        'uwsgi',
        'pytest'
    ],
)
