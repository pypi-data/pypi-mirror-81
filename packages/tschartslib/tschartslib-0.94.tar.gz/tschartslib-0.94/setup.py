from distutils.core import setup
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('tschartslib')

setup(
  name = 'tschartslib',         
  packages = ['tschartslib'],   
  package_data={'': extra_files},
  version = '0.94',      
  license='apache-2.0',       
  description = 'Python API for calling tscharts REST API',  
  author = 'Syd Logan',                  
  author_email = 'slogan621@gmail.com',     
  url = 'https://github.com/slogan621/tscharts',   
  download_url = '',   
  keywords = ['RESTful', 'Medical', 'API'], 
  install_requires=[   
          'requests',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',    
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: Apache Software License', 
    'Programming Language :: Python :: 2',    
    'Programming Language :: Python :: 2.7',  
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
