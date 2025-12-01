import paddlex
import importlib.metadata
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--nvidia', action='store_true', help='Include NVIDIA CUDA and cuDNN dependencies.')

args = parser.parse_args()

user_deps = [dist.metadata["Name"] for dist in importlib.metadata.distributions()]
deps_all = list(paddlex.utils.deps.DEP_SPECS.keys())
deps_need = [dep for dep in user_deps if dep in deps_all]

cmd = [
    "pyinstaller", "main.py",
    "--add-data", "common;common",
    "--add-data", "day_world;day_world",
    "--add-data", "night_world;night_world",
    "--add-data", "style.qss;.",
    "--add-data", "C:\\Miniconda3\\Lib\\site-packages\\Cython\\Utility;Cython/Utility",
    "--icon", "avatar.ico",
    "--collect-data", "paddlex",
    "--collect-binaries", "paddle"
]

if args.nvidia:
    cmd += ["--collect-binaries", "nvidia"]

for dep in deps_need:
    cmd += ["--copy-metadata", dep]

print("PyInstaller command:", " ".join(cmd))

try:
    result = subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print("Installation failed:", e)
    sys.exit(1)
