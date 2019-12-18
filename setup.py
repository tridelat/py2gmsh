import setuptools
from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(name='py2gmsh',
      packages=['py2gmsh'],
      version='4.2.3.1',
      description='Python wrappers to gmsh files with object-oriented syntax',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Tristan de Lataillade',
      author_email='delataillade.tristan@gmail.com',
      url='https://github.com/tridelat/py2gmsh',
      download_url='https://github.com/tridelat/py2gmsh/tarball/v4.2.3.1',
      keywords=['gmsh', 'wrapper', 'mesh', 'python', 'api'],
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
      ],
)
