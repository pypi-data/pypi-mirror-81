from setuptools import setup
import streamsx.toolkits
setup(
  name = 'streamsx.toolkits',
  packages = ['streamsx.toolkits'],
  include_package_data=True,
  version = streamsx.toolkits.__version__,
  description = 'Utility functions for IBM Streams topology applications',
  long_description = open('DESC.txt').read(),
  author = 'IBM Streams @ github.com',
  author_email = 'hegermar@de.ibm.com',
  license='Apache License - Version 2.0',
  url = 'https://github.com/IBMStreams/streamsx.toolkits',
  keywords = ['streams', 'ibmstreams', 'streaming', 'analytics', 'streaming-analytics', 'toolkits'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  install_requires=['streamsx>=1.15.0', 'wget', 'pyOpenSSL==19.0', 'pyJKS==19.0'],
  
  test_suite='nose.collector',
  tests_require=['nose']
)
