%module purpleairapi_base
%feature("autodoc", "0");

%include <stl.i>
%include "purpleairapi_error.i"
%include "purpleairapi_helpers.i"

%feature("python:annotations", "c");

%include "purpleairapi_read.i"
%include "purpleairapi_write.i"
%include "purpleairapi_local.i"
