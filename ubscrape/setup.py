from setuptools import setup

setup(
    name='ubscrape',
    version='0.1.4',
    description='Scrapes Urban Dictionary and stores it locally.',
    url='http://github.com/samuelstevens/ubscrape',
    author='Samuel Stevens',
    author_email='samuel.robert.stevens@gmail.com',
    license='MIT',
    packages=['ubscrape'],
    entry_points={
        'console_scripts': ['ubscrape = ubscrape.command_line:main']
    },
    install_requires=[
        'bs4',
        'requests'
    ],
)
