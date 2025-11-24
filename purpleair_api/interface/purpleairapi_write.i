%module purpleairapi_write
%feature("autodoc", "0");

%include <std_string.i>
%include "purpleairapi_error.i"
%include "purpleairapi_helpers.i"

%feature("kwargs") PurpleAirAPI::PurpleAirWriteAPI::PurpleAirWriteAPI;
%feature("python:annotations", "c");

%{
#include "PurpleAirWriteAPI.hpp"
%}

// Include the header file
%include "../include/PurpleAirWriteAPI.hpp"
