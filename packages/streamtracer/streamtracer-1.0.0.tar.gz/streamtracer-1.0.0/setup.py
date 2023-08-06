import os
import setuptools

# Need to install numpy first
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])


from numpy.distutils.core import setup, Extension
# Don't want to build the fortran on readthedocs
exts = []
if not os.environ.get('READTHEDOCS', None):
    exts += [Extension(name='streamtracer.fortran.streamtracer',
                       sources=['streamtracer/fortran/Streamtracer.f90'],
                       extra_f90_compile_args=['-fopenmp'],
                       extra_link_args=['-fopenmp']
                       ),
             ]

if __name__ == "__main__":
    setup(name='streamtracer',
          version='1.0.0',
          description='Python wrapped fortran to calculate streamlines',
          url='https://github.com/dstansby/streamtracer',
          author='David Stansby, Lars Mejnertsen',
          author_email='dstansby@gmail.com',
          install_requires=['numpy'],
          python_requires='>=3.6',
          packages=['streamtracer'],
          ext_modules=exts,
          include_package_data=True,
          )
