from distutils.core import setup, Extension

encode = Extension('qrencode._qrencode', sources=['qr_encode.c'], libraries=['qrencode'])

setup(name='qrencode',
      version='1.2',
      description='Encodes QR-codes.',
      author='Nick Johnson',
      author_email='arachnid@notdot.net',
      url='http://github.com/Arachnid/pyqrencode/tree/master',
      long_description='''A simple wrapper for the C qrencode library.''',
      packages=['qrencode'],
      ext_modules=[encode],
      requires=['PIL'])

