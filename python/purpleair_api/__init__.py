#!/usr/bin/env python3

"""
Copyright 2024 carlkidcrypto, All rights reserved.
PurpleAir API - Now with C++ backend and SWIG bindings support
"""

import os
import sys
from pathlib import Path

# On Windows, add the directory containing bundled DLLs to the DLL search path
if sys.platform == "win32":
    _pkg_dir = Path(__file__).resolve().parent
    _libs_dir = _pkg_dir / ".purpleair_api.mesonpy.libs"
    if _libs_dir.is_dir():
        try:
            os.add_dll_directory(str(_libs_dir))
        except (AttributeError, OSError):
            pass
    if _pkg_dir.is_dir():
        try:
            os.add_dll_directory(str(_pkg_dir))
        except (AttributeError, OSError):
            pass

# The Python API remains for backward compatibility
# The C++ implementation is used internally via SWIG bindings
