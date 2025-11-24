%module purpleairapi
%feature("autodoc", "0");

%include <std_string.i>
%include <std_map.i>
%include "purpleairapi_base.i"

%feature("kwargs") PurpleAirAPI::PurpleAirAPI::PurpleAirAPI;
%feature("python:annotations", "c");

%{
#include "PurpleAirAPI.hpp"
%}

// Include the header file
%include "../include/PurpleAirAPI.hpp"
