%module purpleairapi_read
%feature("autodoc", "0");

%include <std_string.i>
%include "purpleairapi_error.i"
%include "purpleairapi_helpers.i"

%feature("kwargs") PurpleAirAPI::PurpleAirReadAPI::PurpleAirReadAPI;
%feature("kwargs") PurpleAirAPI::PurpleAirReadAPI::request_sensor_data;
%feature("kwargs") PurpleAirAPI::PurpleAirReadAPI::request_multiple_sensors_data;
%feature("kwargs") PurpleAirAPI::PurpleAirReadAPI::request_sensor_history;
%feature("python:annotations", "c");

%{
#include "PurpleAirReadAPI.h"
%}

// Include the header file
%include "../include/PurpleAirReadAPI.h"
