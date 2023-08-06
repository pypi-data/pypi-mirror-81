from setuptools import setup, find_packages

__version__ = '0.31.2'

setup(
    name="Flask-REST-JSONAPI",
    version=__version__,
    description='Flask extension to create REST web api according to JSONAPI 1.0 specification with Flask, Marshmallow \
                 and data provider of your choice (SQLAlchemy, MongoDB, ...)',
    url='https://github.com/miLibris/flask-rest-jsonapi',
    author='miLibris API Team',
    author_email='pf@milibris.net',
    license='MIT',
    classifiers=[
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='web api rest jsonapi flask sqlalchemy marshmallow',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'six',
        'Flask>=0.11',
        'marshmallow>=3.8.0',
        'marshmallow_jsonapi>=0.23.2',
        'sqlalchemy'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'dev': [
            'pytest',
            'coveralls',
            'coverage'
        ],
        'docs': 'sphinx'
    }
)
