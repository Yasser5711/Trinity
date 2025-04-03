#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent  # one level up from scripts/
VENV_DIR = ROOT_DIR / ".venv"
REQUIREMENTS_FILE = ROOT_DIR / "back" / "requirements.txt"

# Detect OS-specific Python path inside the venv
if os.name == "nt":
    python_exe = VENV_DIR / "Scripts" / "python.exe"
else:
    python_exe = VENV_DIR / "bin" / "python"

if not VENV_DIR.exists():
    print("[+] Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
    print("[✓] .venv created.")

if not REQUIREMENTS_FILE.exists():
    print(f"[!] Cannot find requirements.txt at: {REQUIREMENTS_FILE}")
    sys.exit(1)

print("[+] Installing dev dependencies from back/requirements.txt...")
subprocess.check_call([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])
subprocess.check_call(
    [str(python_exe), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)]
)
print("[✓] Dependencies installed.")
