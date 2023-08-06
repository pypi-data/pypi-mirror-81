from setuptools import setup, find_packages

setup(name='gqrxHamlib',
      version = '3.0.33',
      description = 'gqrx-Hamlib interface',
      url='http://github.com/g0fcu/gqrx-hamlib-gui',
      author='Simon Kennedy',
      license='GPL',
      packages=find_packages(),
      #install_requires=['xmlrpc.client'],
      entry_points={
          'console_scripts': [
               'gqrxHamlib=gqrxHamlib:main'
                  ]
                }
)
