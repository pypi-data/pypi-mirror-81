from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["WordToVec/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-WordToVec-Cy',
    version='1.0.0',
    packages=['WordToVec'],
    package_data={'WordToVec': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/olcaytaner/WordToVec-Cy',
    license='',
    author='olcay',
    author_email='olcaytaner@isikun.edu.tr',
    description='Word2Vec Library',
    install_requires=['NlpToolkit-Corpus-Cy']
)
