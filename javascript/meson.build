# javascript/meson.build
#
# Generates the SWIG C++ wrapper for the JavaScript/Node.js bindings, then
# copies it into the javascript/ source directory where binding.gyp expects it.
#
# Build:
#   meson setup builddir && ninja -C builddir   # generates + copies SWIG wrapper
#   cd javascript && npm install                # installs node-gyp and jest
#   cd javascript && npm run build-gyp          # compiles the native .node addon
#   cd javascript && npm test

if not get_option('javascript_bindings')
  subdir_done()
endif

swig_iface = meson.project_source_root() / 'swig' / 'interface'
swig_inc   = meson.project_source_root() / 'swig' / 'include'

# ── SWIG step ────────────────────────────────────────────────────────────────
# Generates purpleairapi_base_wrap.cxx in the Meson build dir.
js_swig = custom_target(
  'javascript_swig',
  input: swig_iface / 'purpleairapi_base.i',
  output: 'purpleairapi_base_wrap.cxx',
  command: [
    swig,
    '-javascript', '-node', '-c++',
    '-I' + swig_iface,
    '-I' + swig_inc,
    '-outdir', '@OUTDIR@',
    '-o', '@OUTPUT@',
    '@INPUT@',
  ],
  build_by_default: true,
)

# ── Copy to source directory ──────────────────────────────────────────────────
# node-gyp (binding.gyp) expects the wrapper in the javascript/ source dir.
# Pass @INPUT@ as a standalone list element so Meson expands it correctly.
python = find_program('python3', 'python', required: true)

custom_target(
  'javascript_copy_cxx',
  input: js_swig,
  output: 'javascript_cxx_copy.stamp',
  command: [
    python, '-c',
    'import shutil, sys, pathlib; shutil.copy(sys.argv[1], sys.argv[2]); pathlib.Path(sys.argv[3]).touch()',
    '@INPUT@',
    meson.current_source_dir() / 'purpleairapi_base_wrap.cxx',
    '@OUTPUT@',
  ],
  build_by_default: true,
)
