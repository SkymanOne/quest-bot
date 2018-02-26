from setuptools import setup, find_packages

setup(
    name='quest_bot',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
        'peewee',
        'mypy'
    ],
    entry_points='''
        [console_scripts]
        uob=uob:cli
    ''',
    url='',
    license='',
    author='German Nikolishin',
    author_email='',
    description=''
)
