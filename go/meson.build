# go/meson.build
#
# Replaces go/Makefile.
#
# After `ninja -C builddir`, the three files needed by CGO
# (purpleairapi_wrap.cxx, purpleairapi.go, libpurpleairapi.a) are copied into
# go/purpleairapi/ so that plain `go test ./tests/...` works without any
# extra environment variables.
#
# Build:
#   meson setup builddir && ninja -C builddir
#   cd go && go test ./tests/...

if not get_option('go_bindings')
  subdir_done()
endif

python     = find_program('python3', 'python', required: true)
swig_iface = meson.project_source_root() / 'swig' / 'interface'
swig_inc   = meson.project_source_root() / 'swig' / 'include'
go_pkg_src = meson.current_source_dir() / 'purpleairapi'

# ── SWIG step ────────────────────────────────────────────────────────────────
# Outputs purpleairapi_wrap.cxx and purpleairapi.go to the Meson build dir.
go_swig = custom_target(
  'go_swig',
  input: swig_iface / 'purpleairapi_go.i',
  output: ['purpleairapi_wrap.cxx', 'purpleairapi.go'],
  command: [
    swig,
    '-go', '-c++', '-cgo', '-intgosize', '64',
    '-I' + swig_iface,
    '-I' + swig_inc,
    '-outdir', '@OUTDIR@',
    '-o', '@OUTPUT0@',
    '@INPUT@',
  ],
  build_by_default: true,
)

# ── Static library ────────────────────────────────────────────────────────────
# Compile SWIG C++ wrapper + core sources into libpurpleairapi.a.
go_static_lib = static_library(
  'purpleairapi',
  [go_swig[0]] + purpleair_sources,
  include_directories: purpleair_inc,
  dependencies: [libcurl_dep],
  install: false,
)

# ── Copy artifacts to go/purpleairapi/ ───────────────────────────────────────
# CGO uses `#cgo LDFLAGS: -L${SRCDIR} -lpurpleairapi` (see cgo_helpers.go),
# where ${SRCDIR} resolves to go/purpleairapi/.  Copy all three generated
# artifacts there so plain `go test ./tests/...` works without extra env vars.
#
# Pass @INPUT0@, @INPUT1@, and @OUTPUT@ as standalone list elements so that
# Meson expands them correctly; use go_static_lib.full_path() for the library
# path (resolved at configure time) with depends: to enforce build ordering.
custom_target(
  'go_pkg_setup',
  depends: go_static_lib,
  input: [go_swig[0], go_swig[1]],
  output: 'go_pkg_setup.stamp',
  command: [
    python, '-c',
    'import shutil, subprocess, os, sys, pathlib, tempfile\n'
    + '[shutil.copy(s, d) for s, d in ['
    + '(sys.argv[1], sys.argv[3] + "/purpleairapi_wrap.cxx"), '
    + '(sys.argv[2], sys.argv[3] + "/purpleairapi.go")'
    + ']]\n'
    + 'lib=sys.argv[5]; dst=sys.argv[3]+"/libpurpleairapi.a"\n'
    + 'with open(lib,"rb") as _f: thin=(_f.read(8)==b"!<thin>\\n")\n'
    + 'if thin:\n'
    + '  out=subprocess.run(["ar","-t",lib],capture_output=True,text=True,check=True).stdout\n'
    + '  objs=[os.path.normpath(l) for l in out.splitlines() if l.endswith(".o")]\n'
    + '  subprocess.run(["ar","-crs",dst]+sorted(objs),check=True)\n'
    + 'else:\n'
    + '  tmp=tempfile.mkdtemp()\n'
    + '  subprocess.run(["ar","-x",lib],cwd=tmp,check=True)\n'
    + '  objs=[os.path.join(r,f) for r,ds,fs in os.walk(tmp) for f in fs if f.endswith(".o")]\n'
    + '  subprocess.run(["ar","-crs",dst]+sorted(objs),check=True)\n'
    + '  shutil.rmtree(tmp)\n'
    + 'pathlib.Path(sys.argv[4]).touch()',
    '@INPUT0@',
    '@INPUT1@',
    go_pkg_src,
    '@OUTPUT@',
    go_static_lib.full_path(),
  ],
  build_by_default: true,
)
