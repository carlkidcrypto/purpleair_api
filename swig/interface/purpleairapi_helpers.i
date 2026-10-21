%module purpleairapi_helpers
%feature("autodoc", "0");

%include <std_string.i>
%include <std_map.i>
%include "purpleairapi_error.i"

%{
#include "PurpleAirAPIHelpers.h"
%}

// Tell SWIG about our map types
%template(StringMap) std::map<std::string, std::string>;

// Include the header file
%include "../include/PurpleAirAPIHelpers.h"
