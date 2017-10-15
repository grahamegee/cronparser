from setuptools import setup, find_packages

setup(
    name='cronparser',
    version='0.1',
    description='parse crontab lines',
    author='Grahame Gardiner',
    author_email='grahamegee@gmail.com',
    url='https://github.com/grahamegee/cronparser',
    install_requires=[],
    extras_require={
            'test': ['pytest-cov', 'pytest', 'pyyaml'],
    }
)
