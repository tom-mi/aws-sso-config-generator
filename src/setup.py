from setuptools import setup, find_packages

setup(
    name='aws_sso_config_generator',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['generate-aws-sso-config=aws_sso_config_generator.cli:main'],
    },
    install_requires=['boto3'],
)

