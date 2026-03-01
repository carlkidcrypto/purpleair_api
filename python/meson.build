# python/meson.build
# Standalone Meson project for the Python SWIG bindings.
# Used as the build backend by pyproject.toml via meson-python.
#
# Install (preferred):
#   cd python && pip install .
#
# Manual build:
#   cd python && meson setup builddir && ninja -C builddir

project(
  'purpleair_api',
  ['cpp'],
  version: '2.0.0a0',
  license: 'MIT',
  default_options: [
    'cpp_std=c++17',
    'warning_level=2',
  ],
  meson_version: '>=0.64.0',
)

py_mod = import('python')
py     = py_mod.find_installation(pure: false)

libcurl_dep = dependency('libcurl', required: true)
swig        = find_program('swig', required: true)

# Paths to the shared C++ sources (relative to this meson.build)
_swig_src  = '../swig/src'
_swig_inc  = '../swig/include'
_swig_iface = '../swig/interface'

purpleair_sources = files(
  _swig_src / 'PurpleAirAPI.cpp',
  _swig_src / 'PurpleAirAPIHelpers.cpp',
  _swig_src / 'PurpleAirReadAPI.cpp',
  _swig_src / 'PurpleAirWriteAPI.cpp',
  _swig_src / 'PurpleAirLocalAPI.cpp',
)

purpleair_inc = include_directories(_swig_inc, _swig_iface)

# Absolute paths for the SWIG -I flags (resolved from the source root)
swig_inc_abs   = meson.current_source_dir() / _swig_inc
swig_iface_abs = meson.current_source_dir() / _swig_iface

# ── SWIG step ─────────────────────────────────────────────────────────────────
# Generates purpleairapi_base_wrap.cpp (C++) and purpleairapi_base.py (Python).
python_swig = custom_target(
  'python_swig',
  input: meson.current_source_dir() / _swig_iface / 'purpleairapi_base.i',
  output: ['purpleairapi_base_wrap.cpp', 'purpleairapi_base.py'],
  command: [
    swig,
    '-c++', '-python', '-py3',
    '-I' + swig_iface_abs,
    '-I' + swig_inc_abs,
    '-outdir', '@OUTDIR@',
    '-o', '@OUTPUT0@',
    '@INPUT@',
  ],
)

# ── Python extension module (_purpleairapi_base.so / .pyd) ───────────────────
py.extension_module(
  '_purpleairapi_base',
  [python_swig[0]] + purpleair_sources,
  include_directories: purpleair_inc,
  dependencies: [py.dependency(), libcurl_dep],
  install: true,
  subdir: 'purpleair_api',
)

# ── Install generated purpleairapi_base.py ───────────────────────────────────
py.install_sources(
  python_swig[1],
  subdir: 'purpleair_api',
)

# ── Install hand-written Python source files ─────────────────────────────────
py.install_sources(
  [
    'purpleair_api/__init__.py',
    'purpleair_api/PurpleAirAPI.py',
    'purpleair_api/PurpleAirAPIConstants.py',
    'purpleair_api/PurpleAirAPIError.py',
    'purpleair_api/PurpleAirAPIHelpers.py',
    'purpleair_api/PurpleAirLocalAPI.py',
    'purpleair_api/PurpleAirReadAPI.py',
    'purpleair_api/PurpleAirWriteAPI.py',
  ],
  subdir: 'purpleair_api',
)
