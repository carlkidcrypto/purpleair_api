%module purpleairapi_local
%feature("autodoc", "0");

%include <std_string.i>
%include <std_vector.i>
%include "purpleairapi_error.i"
%include "purpleairapi_helpers.i"

%feature("kwargs") PurpleAirAPI::PurpleAirLocalAPI::PurpleAirLocalAPI;
%feature("python:annotations", "c");

%{
#include "PurpleAirLocalAPI.h"
%}

// Tell SWIG about our vector types
%template(StringVector) std::vector<std::string>;

// Include the header file
%include "../include/PurpleAirLocalAPI.h"
