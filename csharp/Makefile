# Makefile for building C# PurpleAir API

CXX = g++
SWIG = swig
CXXFLAGS = -std=c++17 -fPIC -shared
INCLUDES = -I../swig/include
LIBS = -lcurl

# SWIG interface file
SWIG_INTERFACE = ../swig/interface/purpleairapi_base.i
SWIG_WRAP = purpleairapi_base_wrap.cxx

# C++ source files
CPP_SOURCES = ../swig/src/PurpleAirAPI.cpp \
              ../swig/src/PurpleAirAPIHelpers.cpp \
              ../swig/src/PurpleAirReadAPI.cpp \
              ../swig/src/PurpleAirWriteAPI.cpp \
              ../swig/src/PurpleAirLocalAPI.cpp

TARGET = libpurpleairapi.so

# Generated C# files
CS_FILES = purpleairapi_base.cs purpleairapi_basePINVOKE.cs \
           PurpleAirAPIError.cs PurpleAirLocalAPI.cs \
           PurpleAirReadAPI.cs PurpleAirWriteAPI.cs \
           StringMap.cs _string_vector.cs

all: swig $(TARGET)

# Generate SWIG wrapper and C# files
swig: $(SWIG_WRAP)

$(SWIG_WRAP): $(SWIG_INTERFACE)
	$(SWIG) -c++ -csharp -namespace PurpleAirAPI \
		-I../swig/interface -I../swig/include \
		-outdir . -o $(SWIG_WRAP) $(SWIG_INTERFACE)

$(TARGET): $(SWIG_WRAP) $(CPP_SOURCES)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(CPP_SOURCES) $(SWIG_WRAP) $(LIBS) -o $(TARGET)

clean:
	rm -f $(TARGET) $(SWIG_WRAP) $(CS_FILES)

.PHONY: all swig clean
