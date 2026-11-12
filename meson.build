project(
  'purpleair_api',
  ['cpp'],
  version: '2026.11.11a2',
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
cpp = meson.get_compiler('cpp')
if host_machine.system() == 'darwin'
  libcurl_dep = cpp.find_library('curl', required: true)
else
  libcurl_dep = dependency('libcurl', required: false)
  if not libcurl_dep.found()
    libcurl_dep = cpp.find_library('curl', required: true)
  endif
endif
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
