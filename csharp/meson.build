# csharp/meson.build
#
# Replaces csharp/Makefile.
#
# The SWIG wrapper (.cxx) and generated C# files (.cs) are placed in the Meson
# build directory.  `dotnet build` is told where to find them via the
# GeneratedSourcesDir MSBuild property (see PurpleAirAPI.csproj).
#
# Build:
#   meson setup builddir && ninja -C builddir
#   dotnet build csharp/PurpleAirAPI.csproj \
#       --configuration Release \
#       -p:GeneratedSourcesDir=$(pwd)/builddir/csharp/
#   dotnet test csharp/tests/Tests.csproj \
#       --configuration Release \
#       -p:GeneratedSourcesDir=$(pwd)/builddir/csharp/

if not get_option('csharp_bindings')
  subdir_done()
endif

swig_iface = meson.project_source_root() / 'swig' / 'interface'
swig_inc   = meson.project_source_root() / 'swig' / 'include'

# ── SWIG step ────────────────────────────────────────────────────────────────
# All outputs land in the Meson build dir (builddir/csharp/).
# dotnet is pointed at them via -p:GeneratedSourcesDir=<builddir>/csharp/.
csharp_swig = custom_target(
  'csharp_swig',
  input: swig_iface / 'purpleairapi_base.i',
  output: [
    'purpleairapi_base_wrap.cxx',
    'purpleairapi_base.cs',
    'purpleairapi_basePINVOKE.cs',
    'PurpleAirAPIError.cs',
    'PurpleAirLocalAPI.cs',
    'PurpleAirReadAPI.cs',
    'PurpleAirWriteAPI.cs',
    'StringMap.cs',
    '_string_vector.cs',
  ],
  command: [
    swig,
    '-c++', '-csharp',
    '-namespace', 'PurpleAirAPI',
    '-I' + swig_iface,
    '-I' + swig_inc,
    '-outdir', '@OUTDIR@',
    '-o', '@OUTPUT0@',
    '@INPUT@',
  ],
  build_by_default: true,
)

# ── Native shared library ─────────────────────────────────────────────────────
# Compile the SWIG C++ wrapper + core C++ sources into libpurpleairapi.so.
# dotnet loads this at runtime via P/Invoke.
shared_library(
  'purpleairapi_base',
  [csharp_swig[0]] + purpleair_sources,
  include_directories: purpleair_inc,
  dependencies: [libcurl_dep],
  install: false,
)
