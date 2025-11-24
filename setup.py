#!/usr/bin/env python3
"""
PurpleAir API - Multi-language wrapper with C++ backend

This is the root setup.py that delegates to language-specific builds.
For Python-specific build, use: python -m pip install ./python
"""

import os
import sys
import subprocess

# Delegate to Python build by default
if __name__ == '__main__':
    python_dir = os.path.join(os.path.dirname(__file__), 'python')
    os.chdir(python_dir)
    sys.exit(subprocess.call([sys.executable, 'setup.py'] + sys.argv[1:]))
