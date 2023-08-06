from setuptools import setup, find_packages
 
setup(name='kea_bigquery_connection',
      version='1.1',
      url='http://kea.mx/',
      packages=find_packages(exclude=['tests']),	
      license='MIT',
      author='Daniel Hernández',
      author_email='dhernandez@kea.mx',
      description='Run queries in bigquery and get a data response',
      zip_safe=False)