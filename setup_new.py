#!/usr/bin/env python3

import os
import sys
from subprocess import check_output, CalledProcessError
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Get version from setup.cfg or use default
VERSION = "1.3.1"

def get_include_dirs():
    """Get include directories for compilation."""
    include_dirs = [
        "purpleair_api/include",
        "/usr/include",
        "/usr/local/include"
    ]
    
    # Check for curl include directory
    try:
        curl_config = check_output(["pkg-config", "--cflags-only-I", "libcurl"]).decode().strip()
        if curl_config:
            curl_includes = [i[2:] for i in curl_config.split() if i.startswith("-I")]
            include_dirs.extend(curl_includes)
    except (CalledProcessError, FileNotFoundError):
        # Fallback to standard locations
        pass
    
    return include_dirs

def get_library_dirs():
    """Get library directories for linking."""
    library_dirs = [
        "/usr/lib",
        "/usr/local/lib",
        "/usr/lib/x86_64-linux-gnu"
    ]
    
    # Check for curl library directory
    try:
        curl_config = check_output(["pkg-config", "--libs-only-L", "libcurl"]).decode().strip()
        if curl_config:
            curl_libs = [i[2:] for i in curl_config.split() if i.startswith("-L")]
            library_dirs.extend(curl_libs)
    except (CalledProcessError, FileNotFoundError):
        pass
    
    return library_dirs

def get_libraries():
    """Get libraries to link against."""
    return ["curl"]

class CustomBuildExt(build_ext):
    """Custom build_ext command to handle SWIG."""
    
    def run(self):
        # Run SWIG to generate wrapper code
        for ext in self.extensions:
            if ext.swig_opts:
                self.swig_sources(ext.sources, ext)
        
        # Continue with normal build
        build_ext.run(self)

# Define the C++ extension module
purpleairapi_extension = Extension(
    name='_purpleairapi_base',
    sources=[
        'purpleair_api/src/PurpleAirAPIHelpers.cpp',
        'purpleair_api/src/PurpleAirReadAPI.cpp',
        'purpleair_api/src/PurpleAirWriteAPI.cpp',
        'purpleair_api/src/PurpleAirLocalAPI.cpp',
        'purpleair_api/src/PurpleAirAPI.cpp',
        'purpleair_api/interface/purpleairapi_base.i',
    ],
    include_dirs=get_include_dirs(),
    library_dirs=get_library_dirs(),
    libraries=get_libraries(),
    swig_opts=[
        '-c++',
        '-python',
        '-py3',
        '-Ipurpleair_api/interface',
        '-Ipurpleair_api/include',
        '-outdir', 'purpleair_api',
    ],
    extra_compile_args=['-std=c++11', '-fPIC'],
    language='c++',
)

setup(
    name='purpleair_api',
    version=VERSION,
    author='Carlos Santos',
    author_email='dose.lucky.sake@cloak.id',
    description='PurpleAir API wrapper with C++ backend and SWIG bindings',
    long_description=open('README.rst').read() if os.path.exists('README.rst') else '',
    long_description_content_type='text/x-rst',
    url='https://github.com/carlkidcrypto/purpleair_api',
    packages=['purpleair_api'],
    ext_modules=[purpleairapi_extension],
    cmdclass={'build_ext': CustomBuildExt},
    install_requires=[],
    python_requires='>=3.9,<3.14',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: C++',
    ],
)
