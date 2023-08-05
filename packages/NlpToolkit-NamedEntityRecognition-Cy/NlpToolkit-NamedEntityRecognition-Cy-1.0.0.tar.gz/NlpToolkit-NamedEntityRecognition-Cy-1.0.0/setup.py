from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["NamedEntityRecognition/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-NamedEntityRecognition-Cy',
    version='1.0.0',
    packages=['NamedEntityRecognition'],
    package_data={'NamedEntityRecognition': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/olcaytaner/TurkishNamedEntityRecognition-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='NER Corpus Processing Library',
    install_requires=['NlpToolkit-Corpus-Cy']
)
