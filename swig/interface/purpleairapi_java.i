%module purpleairapi_base
%feature("autodoc", "0");

%pragma(java) jniclasscode=%{
  static {
    try {
      System.loadLibrary("purpleairapi_base_java");
    } catch (UnsatisfiedLinkError e) {
      // Allow manual loading or explicit System.load() fallback
    }
  }
%}

%include "purpleairapi_base.i"
