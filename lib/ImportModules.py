import sys, subprocess, os

def import_pymongo_from_venv(venv_dir="MyScriptVenv"):
    sys.path = [p for p in sys.path if venv_dir not in p]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(base_dir, venv_dir)
    if not os.path.isdir(venv_path):
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = os.path.join(venv_path, "lib", python_version, "site-packages")
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)
    try:
        import pymongo
        return pymongo
    except ImportError:
        pip_executable = os.path.join(venv_path, "bin", "pip")
        subprocess.check_call([pip_executable, "install", "pymongo"])
        import pymongo
        return pymongo