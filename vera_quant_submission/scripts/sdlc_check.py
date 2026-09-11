import subprocess, sys
commands = [[sys.executable, "-m", "pytest", "-q"]]
for cmd in commands:
    print("$", " ".join(cmd))
    raise SystemExit(subprocess.call(cmd))
