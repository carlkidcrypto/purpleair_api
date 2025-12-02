{
  "targets": [
    {
      "target_name": "purpleairapi_base",
      "sources": [
        "purpleairapi_base_wrap.cxx",
        "../swig/src/PurpleAirAPI.cpp",
        "../swig/src/PurpleAirAPIHelpers.cpp",
        "../swig/src/PurpleAirReadAPI.cpp",
        "../swig/src/PurpleAirWriteAPI.cpp",
        "../swig/src/PurpleAirLocalAPI.cpp"
      ],
      "include_dirs": [
        "../swig/include"
      ],
      "libraries": [
        "-lcurl"
      ],
      "cflags!": [ "-fno-exceptions" ],
      "cflags_cc!": [ "-fno-exceptions" ],
      "cflags": [ "-std=c++17" ],
      "cflags_cc": [ "-std=c++17" ],
      "conditions": [
        ["OS=='mac'", {
          "xcode_settings": {
            "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
            "CLANG_CXX_LIBRARY": "libc++",
            "MACOSX_DEPLOYMENT_TARGET": "10.7",
            "OTHER_CPLUSPLUSFLAGS": [
              "-std=c++17",
              "-stdlib=libc++"
            ]
          }
        }]
      ]
    }
  ]
}
