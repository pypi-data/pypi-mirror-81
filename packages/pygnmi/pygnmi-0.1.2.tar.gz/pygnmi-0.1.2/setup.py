from distutils.core import setup
setup(
  name = 'pygnmi',
  packages = ['pygnmi'],
  version = '0.1.2',
  license='bsd-3-clause',
  description = 'This repository contains pure Python implementation of the gNMI client to interact with the network functions.',
  author = 'Anton Karneliuk',
  author_email = 'anton@karneliuk.com',
  url = 'https://github.com/akarneliuk/pygnmi',
  download_url = 'https://github.com/akarneliuk/pygnmi/archive/v0.1.2.tar.gz',
  keywords = ['gnmi', 'automation', 'grpc', 'network'], 
  install_requires=[
          'grpcio',
          'grpcio-tools'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Telecommunications Industry',
    'Operating System :: OS Independent',
    'Topic :: System :: Networking',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)