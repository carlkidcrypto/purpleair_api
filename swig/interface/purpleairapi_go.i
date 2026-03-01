%module purpleairapi
%feature("autodoc", "0");

// Rename STL template types to Go-exported names (must come before %template definitions)
%rename("StringVector") _string_vector;
%rename("StringMap") _string_map;

%include "purpleairapi_base.i"
