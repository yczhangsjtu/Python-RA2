from distutils.core import setup, Extension

module1 = Extension('shpfile',
                    sources = ['shpfile.c'])

setup (name = 'shpfile',
       version = '1.0',
       description = 'This is a package used for reading .shp file.',
       ext_modules = [module1])


