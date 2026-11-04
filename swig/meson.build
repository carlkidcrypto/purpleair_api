# swig/meson.build
# Standalone C++ shared library for direct C++ consumption.
# Each language binding also compiles the same C++ sources into its own native
# library so this target is only useful when you want to link C++ code directly.

shared_library(
  'purpleairapi',
  purpleair_sources,
  include_directories: purpleair_inc,
  dependencies: [libcurl_dep],
  install: false,
)
