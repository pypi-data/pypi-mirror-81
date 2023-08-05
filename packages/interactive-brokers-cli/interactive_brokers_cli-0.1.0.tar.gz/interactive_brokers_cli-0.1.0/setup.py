'''
Setup configuration for the package.
'''
from setuptools import setup, find_packages

setup(name='interactive_brokers_cli',
      version='0.1.0',
      packages=find_packages(),
      license='GPL3',
      # zip_safe=False,
      install_requires=['click', 'click_log'],
      package_data={"": ["default_config.yaml"]},
      # metadata to display on PyPI
      author='Alen Šiljak',
      author_email='ibcli@alensiljak.eu.org',
      description='CLI for fetching and parsing IB Flex Queries',
      keywords="interactive brokers cli flex queries",
      url='https://gitlab.com/alensiljak/interactive-brokers-cli',
      project_urls={
          "Source Code": "https://gitlab.com/alensiljak/interactive-brokers-cli.git"
      },
      # Scripts
      entry_points={
          "console_scripts": [
              "ib = ibcli.cli:cli"
          ]
      }
      )
