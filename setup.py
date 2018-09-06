from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(name = 'py2gmsh',
      packages = ['py2gmsh'],
      version = 'v3.0.6.0',
      description = 'Python wrappers to gmsh files with object-oriented syntax',
      long_description = long_description,
      author = 'Tristan de Lataillade',
      author_email = 'delataillade.tristan@gmail.com',
      url = 'https://github.com/tridelat/py2gmsh',
      download_url = 'https://github.com/tridelat/py2gmsh/tarball/v3.0.6.0',
      keywords = ['gmsh', 'wrapper', 'mesh', 'python', 'api'],
      classifiers = [])
