from setuptools import setup

setup(
    name='sreserver',
    version='1.0',
    long_description=__doc__,
    packages=['sreserver'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'flask-bootstrap',
        'flask-appconfig',
        'requests',
        'flask-nav',
        'yaml',
        ],
)
