project(
  'purpleair_api',
  ['cpp'],
  version: '2.0.0.a0',
  license: 'MIT',
  default_options: [
    'cpp_std=c++17',
    'warning_level=2',
  ],
  meson_version: '>=0.64.0',
)

# ---------------------------------------------------------------------------
# Common dependencies and tools
# ---------------------------------------------------------------------------
libcurl_dep = dependency('libcurl', required: true)
swig = find_program('swig', required: true)

# ---------------------------------------------------------------------------
# Core C++ sources and include paths (shared across all language bindings)
# ---------------------------------------------------------------------------
purpleair_sources = files(
  'swig/src/PurpleAirAPI.cpp',
  'swig/src/PurpleAirAPIHelpers.cpp',
  'swig/src/PurpleAirReadAPI.cpp',
  'swig/src/PurpleAirWriteAPI.cpp',
  'swig/src/PurpleAirLocalAPI.cpp',
)

purpleair_inc = include_directories('swig/include', 'swig/interface')

# ---------------------------------------------------------------------------
# Subprojects
# ---------------------------------------------------------------------------

# C++ core library (standalone usage)
subdir('swig')

# C# native bindings
subdir('csharp')

# Go bindings
subdir('go')

# JavaScript/Node.js bindings
subdir('javascript')
