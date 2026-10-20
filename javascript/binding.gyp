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
        "<!@(node -p \"require('node-addon-api').include\")",
        "../swig/include"
      ],
      "defines": [
        "NAPI_CPP_EXCEPTIONS"
      ],
      "cflags!": [ "-fno-exceptions" ],
      "cflags_cc!": [ "-fno-exceptions" ],
      "cflags": [ "-std=c++20" ],
      "cflags_cc": [ "-std=c++20" ],
      "conditions": [
        ["OS!='win'", {
          "libraries": [
            "-lcurl"
          ]
        }],
        ["OS=='mac'", {
          "xcode_settings": {
            "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
            "CLANG_CXX_LIBRARY": "libc++",
            "MACOSX_DEPLOYMENT_TARGET": "10.15",
            "OTHER_CPLUSPLUSFLAGS": [
              "-std=c++20",
              "-stdlib=libc++"
            ]
          }
        }],
        ["OS=='win'", {
          "defines": [
            "_HAS_EXCEPTIONS=1"
          ],
          "msvs_settings": {
            "VCCLCompilerTool": {
              "ExceptionHandling": 1
            }
          },
          "include_dirs": [
            "<!@(node -p \"(process.env.VCPKG_INSTALLATION_ROOT || 'C:/vcpkg').replace(/\\\\\\\\/g, '/') + '/installed/x64-windows/include'\")"
          ],
          "libraries": [
            "-l<!@(node -p \"(process.env.VCPKG_INSTALLATION_ROOT || 'C:/vcpkg').replace(/\\\\\\\\/g, '/') + '/installed/x64-windows/lib/curl.lib'\")"
          ]
        }]
      ]
    }
  ]
}
