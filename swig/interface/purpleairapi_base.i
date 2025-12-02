%module purpleairapi_base
%feature("autodoc", "0");

%include <stl.i>
%include "purpleairapi_error.i"
%include "purpleairapi_helpers.i"

%feature("python:annotations", "c");

// Tell SWIG how to handle our special return type(s) from C++
%template(_string_map) std::map<std::string, std::string>;
%template(_string_vector) std::vector<std::string>;

%include "purpleairapi_read.i"
%include "purpleairapi_write.i"
%include "purpleairapi_local.i"
