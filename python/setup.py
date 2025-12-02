#!/usr/bin/env python3
"""
Setup script for purpleair_api Python bindings.
Supports macOS, Linux, and Windows.
"""

import os
import sys
import platform
from subprocess import check_output, CalledProcessError
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


def get_version():
    """Read version from pyproject.toml."""
    return "1.4.0a1"


def get_swig_base():
    """Get absolute path to swig directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'swig'))


def get_include_dirs():
    """Get include directories for compilation based on platform."""
    swig_base = get_swig_base()
    include_dirs = [os.path.join(swig_base, 'include')]
    
    system = platform.system()
    
    if system == 'Linux':
        include_dirs.extend(["/usr/include", "/usr/local/include"])
        # Try pkg-config for libcurl
        try:
            curl_config = check_output(["pkg-config", "--cflags-only-I", "libcurl"]).decode().strip()
            if curl_config:
                curl_includes = [i[2:] for i in curl_config.split() if i.startswith("-I")]
                include_dirs.extend(curl_includes)
        except (CalledProcessError, FileNotFoundError):
            pass
            
    elif system == 'Darwin':  # macOS
        # Homebrew paths
        include_dirs.extend([
            "/usr/local/include",
            "/opt/homebrew/include",
            "/opt/homebrew/opt/curl/include",
        ])
        # Try pkg-config for libcurl
        try:
            curl_config = check_output(["pkg-config", "--cflags-only-I", "libcurl"]).decode().strip()
            if curl_config:
                curl_includes = [i[2:] for i in curl_config.split() if i.startswith("-I")]
                include_dirs.extend(curl_includes)
        except (CalledProcessError, FileNotFoundError):
            pass
            
    elif system == 'Windows':
        # vcpkg or manual curl installation paths
        vcpkg_root = os.environ.get('VCPKG_ROOT', 'C:\\vcpkg')
        include_dirs.extend([
            os.path.join(vcpkg_root, 'installed', 'x64-windows', 'include'),
            'C:\\curl\\include',
        ])
    
    return [d for d in include_dirs if os.path.exists(d) or d == os.path.join(swig_base, 'include')]


def get_library_dirs():
    """Get library directories for linking based on platform."""
    library_dirs = []
    system = platform.system()
    
    if system == 'Linux':
        library_dirs.extend([
            "/usr/lib",
            "/usr/local/lib",
            "/usr/lib/x86_64-linux-gnu",
            "/usr/lib/aarch64-linux-gnu",
        ])
        try:
            curl_config = check_output(["pkg-config", "--libs-only-L", "libcurl"]).decode().strip()
            if curl_config:
                curl_libs = [i[2:] for i in curl_config.split() if i.startswith("-L")]
                library_dirs.extend(curl_libs)
        except (CalledProcessError, FileNotFoundError):
            pass
            
    elif system == 'Darwin':  # macOS
        library_dirs.extend([
            "/usr/local/lib",
            "/opt/homebrew/lib",
            "/opt/homebrew/opt/curl/lib",
        ])
        try:
            curl_config = check_output(["pkg-config", "--libs-only-L", "libcurl"]).decode().strip()
            if curl_config:
                curl_libs = [i[2:] for i in curl_config.split() if i.startswith("-L")]
                library_dirs.extend(curl_libs)
        except (CalledProcessError, FileNotFoundError):
            pass
            
    elif system == 'Windows':
        vcpkg_root = os.environ.get('VCPKG_ROOT', 'C:\\vcpkg')
        library_dirs.extend([
            os.path.join(vcpkg_root, 'installed', 'x64-windows', 'lib'),
            'C:\\curl\\lib',
        ])
    
    return [d for d in library_dirs if os.path.exists(d)]


def get_libraries():
    """Get libraries to link against based on platform."""
    system = platform.system()
    
    if system == 'Windows':
        return ["libcurl"]
    else:
        return ["curl"]


def get_extra_compile_args():
    """Get extra compile arguments based on platform."""
    system = platform.system()
    
    if system == 'Windows':
        return ['/std:c++17', '/EHsc']
    else:
        return ['-std=c++17', '-fPIC']


def get_extra_link_args():
    """Get extra link arguments based on platform."""
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        return ['-stdlib=libc++']
    elif system == 'Windows':
        return []
    else:
        return []


class CustomBuildExt(build_ext):
    """Custom build_ext command to handle SWIG and cross-platform builds."""
    
    def run(self):
        # Run SWIG to generate wrapper code
        for ext in self.extensions:
            if ext.swig_opts:
                self.swig_sources(ext.sources, ext)
        
        # Continue with normal build
        build_ext.run(self)


# Define the C++ extension module
swig_base = get_swig_base()

purpleairapi_extension = Extension(
    name='_purpleairapi_base',
    sources=[
        os.path.join(swig_base, 'src', 'PurpleAirAPIHelpers.cpp'),
        os.path.join(swig_base, 'src', 'PurpleAirReadAPI.cpp'),
        os.path.join(swig_base, 'src', 'PurpleAirWriteAPI.cpp'),
        os.path.join(swig_base, 'src', 'PurpleAirLocalAPI.cpp'),
        os.path.join(swig_base, 'src', 'PurpleAirAPI.cpp'),
        os.path.join(swig_base, 'interface', 'purpleairapi_base.i'),
    ],
    include_dirs=get_include_dirs(),
    library_dirs=get_library_dirs(),
    libraries=get_libraries(),
    swig_opts=[
        '-c++',
        '-python',
        '-py3',
        '-I' + os.path.join(swig_base, 'interface'),
        '-I' + os.path.join(swig_base, 'include'),
        '-outdir', 'purpleair_api',
    ],
    extra_compile_args=get_extra_compile_args(),
    extra_link_args=get_extra_link_args(),
    language='c++',
)

setup(
    name='purpleair_api',
    version=get_version(),
    author='Carlos Santos',
    author_email='dose.lucky.sake@cloak.id',
    description='PurpleAir API wrapper with C++ backend and SWIG bindings',
    long_description=open('../README.rst').read() if os.path.exists('../README.rst') else '',
    long_description_content_type='text/x-rst',
    url='https://github.com/carlkidcrypto/purpleair_api',
    packages=['purpleair_api'],
    ext_modules=[purpleairapi_extension],
    cmdclass={'build_ext': CustomBuildExt},
    install_requires=['requests'],
    python_requires='>=3.10,<3.15',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
)
