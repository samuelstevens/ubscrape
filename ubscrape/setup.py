from setuptools import setup

setup(
    # This is the name of your PyPI-package.
    name='ubscrape',
    # Update the version number for new releases
    version='0.2',
    description='Scrapes Urban Dictionary and stores it locally.',
    url='http://github.com/samuelstevens/ubscrape',
    author='Samuel Stevens',
    author_email='samuel.robert.stevens@gmail.com',
    license='MIT',
    packages=['ubscrape'],
    entry_points={
        'console_scripts': ['ubscrape = ubscrape.command_line:main']
    }
)
