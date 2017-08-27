from setuptools import setup, find_packages

setup(
    name='csmon',

    version='0.1.0',

    description='CS Monitoring Application',
    long_description="CS Monitoring Application can take in an input of URLs "
                     "and monitors each URL.",
    url='https://www.google.com',
    author='sa2018',
    author_email='sa@sa2018.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='monitoring devops',

    packages=find_packages(exclude=['bin', 'docs', 'tests']),

    install_requires=[
                      'requests>=2',
                     ],

    extras_require={
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'csmon=csmon.cli:Cli',

        ],
    },
)
