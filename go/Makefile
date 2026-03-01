# Makefile for building Go PurpleAir API bindings

CXX = g++
SWIG = swig
CXXFLAGS = -std=c++17 -fPIC
INCLUDES = -I../swig/include
LIBS = -lcurl

# SWIG interface file
SWIG_INTERFACE = ../swig/interface/purpleairapi_go.i

# Output files
SWIG_WRAP = purpleairapi/purpleairapi_wrap.cxx
GO_WRAP = purpleairapi/purpleairapi.go
STATIC_LIB = purpleairapi/libpurpleairapi.a

# C++ source files
CPP_SOURCES = ../swig/src/PurpleAirAPI.cpp \
              ../swig/src/PurpleAirAPIHelpers.cpp \
              ../swig/src/PurpleAirReadAPI.cpp \
              ../swig/src/PurpleAirWriteAPI.cpp \
              ../swig/src/PurpleAirLocalAPI.cpp

CPP_OBJECTS = PurpleAirAPI.o \
              PurpleAirAPIHelpers.o \
              PurpleAirReadAPI.o \
              PurpleAirWriteAPI.o \
              PurpleAirLocalAPI.o

all: $(STATIC_LIB) $(SWIG_WRAP)

# Generate SWIG Go wrapper
$(SWIG_WRAP): $(SWIG_INTERFACE)
	$(SWIG) -go -c++ -cgo -intgosize 64 \
		-I../swig/interface -I../swig/include \
		-outdir purpleairapi/ \
		-o $(SWIG_WRAP) \
		$(SWIG_INTERFACE)

# Build static library from C++ sources
$(STATIC_LIB): $(CPP_OBJECTS)
	ar rcs $@ $(CPP_OBJECTS)

PurpleAirAPI.o: ../swig/src/PurpleAirAPI.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

PurpleAirAPIHelpers.o: ../swig/src/PurpleAirAPIHelpers.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

PurpleAirReadAPI.o: ../swig/src/PurpleAirReadAPI.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

PurpleAirWriteAPI.o: ../swig/src/PurpleAirWriteAPI.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

PurpleAirLocalAPI.o: ../swig/src/PurpleAirLocalAPI.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

build: all
	go build ./...

test: all
	go test ./tests/...

clean:
	rm -f $(SWIG_WRAP) $(GO_WRAP) $(STATIC_LIB) $(CPP_OBJECTS)
	go clean ./... 2>/dev/null || true

.PHONY: all build test clean
