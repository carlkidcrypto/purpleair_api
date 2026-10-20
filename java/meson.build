# java/meson.build
#
# Build definitions for Java SWIG bindings.
#
# Generates com.purpleair.api Java classes and libpurpleairapi_base_java.so,
# compiles them into purpleair-api.jar, and tests them via Meson's test runner.
#
# Build:
#   meson setup builddir && ninja -C builddir
#
# Test:
#   meson test -C builddir java_tests -v

if not get_option('enable_java_bindings')
  subdir_done()
endif

jni_dep = dependency('jni', required: false)
if not jni_dep.found()
  message('JNI dependency not found; skipping Java bindings.')
  subdir_done()
endif

java_prog = find_program('java', required: false)
javac_prog = find_program('javac', required: false)
jar_prog = find_program('jar', required: false)
python = find_program('python3', 'python', required: true)

if not java_prog.found() or not javac_prog.found() or not jar_prog.found()
  message('Java runtime/compiler tools (java, javac, jar) not found; skipping Java bindings.')
  subdir_done()
endif

swig_iface = meson.project_source_root() / 'swig' / 'interface'
swig_inc   = meson.project_source_root() / 'swig' / 'include'
build_jar_script = meson.current_source_dir() / 'build_jar.py'

# ── SWIG step and JAR compilation ───────────────────────────────────────────
# Generates purpleairapi_base_wrap.cpp and purpleair-api.jar
java_swig_jar = custom_target(
  'java_swig_jar',
  input: swig_iface / 'purpleairapi_java.i',
  output: [
    'purpleairapi_base_wrap.cpp',
    'purpleair-api.jar',
  ],
  command: [
    python,
    build_jar_script,
    swig,
    javac_prog,
    jar_prog,
    swig_iface,
    swig_inc,
    '@OUTPUT0@',
    '@OUTPUT1@',
    '@INPUT@',
  ],
  build_by_default: true,
)

# ── JNI native shared library ─────────────────────────────────────────────────
libpurpleairapi_base_java = shared_library(
  'purpleairapi_base_java',
  [java_swig_jar[0]] + purpleair_sources,
  include_directories: purpleair_inc,
  dependencies: [jni_dep, libcurl_dep],
  install: false,
)

# ── Java Unit Test ───────────────────────────────────────────────────────────
java_test_src = files('tests/PurpleAirAPITest.java')
test_jar = custom_target(
  'java_test_jar',
  input: java_test_src,
  output: 'purpleair-api-tests.jar',
  command: [
    python, '-c',
    'import os, subprocess, sys, tempfile, shutil\n'
    + 'javac=sys.argv[1]; jar=sys.argv[2]; api_jar=sys.argv[3]; test_src=sys.argv[4]; out_jar=sys.argv[5]\n'
    + 'tmp=tempfile.mkdtemp()\n'
    + 'try:\n'
    + '  subprocess.run([javac, "-cp", api_jar, "-d", tmp, test_src], check=True)\n'
    + '  subprocess.run([jar, "cf", os.path.abspath(out_jar), "-C", tmp, "."], check=True)\n'
    + 'finally:\n'
    + '  shutil.rmtree(tmp, ignore_errors=True)',
    javac_prog,
    jar_prog,
    java_swig_jar[1],
    '@INPUT@',
    '@OUTPUT@',
  ],
  build_by_default: true,
)

test(
  'java_tests',
  java_prog,
  args: [
    '-Djava.library.path=' + meson.current_build_dir(),
    '-cp',
    java_swig_jar[1].full_path() + ':' + test_jar.full_path(),
    'PurpleAirAPITest',
  ],
  depends: [libpurpleairapi_base_java, java_swig_jar, test_jar],
  workdir: meson.current_build_dir(),
)
