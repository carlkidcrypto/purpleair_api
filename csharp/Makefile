# Makefile for building C# PurpleAir API

CXX = g++
CXXFLAGS = -std=c++17 -fPIC -shared
INCLUDES = -I../swig/include
LIBS = -lcurl

SOURCES = ../swig/src/PurpleAirAPI.cpp \
          ../swig/src/PurpleAirAPIHelpers.cpp \
          ../swig/src/PurpleAirReadAPI.cpp \
          ../swig/src/PurpleAirWriteAPI.cpp \
          ../swig/src/PurpleAirLocalAPI.cpp \
          purpleairapi_base_wrap.cxx

TARGET = libpurpleairapi.so

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SOURCES) $(LIBS) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
