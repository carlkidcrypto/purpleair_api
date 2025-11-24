%module purpleairapi_error
%feature("autodoc", "0");

%include <std_string.i>
%include <exception.i>

%{
#include "PurpleAirAPIError.hpp"
%}

// Handle C++ exceptions in Python
%exception {
    try {
        $action
    } catch (const PurpleAirAPI::PurpleAirAPIError& e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch (const std::exception& e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch (...) {
        SWIG_exception(SWIG_RuntimeError, "Unknown exception");
    }
}

// Include the header file
%include "../include/PurpleAirAPIError.hpp"
