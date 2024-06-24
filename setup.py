import sys
# import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["sounddevice", "tensorflow", "numpy"],
    "excludes": ["cx_Freeze",
                 "email",
                 "html",
                 "urll",
                 "radon"],
    'include_files': ["resource"],
    # "path": sys.path + [f"{os.getcwd()}/src"],
}

bdist_mac_options = {
    # "iconfile": "resource/icon.ico",
    "bundle_name": "AudioIdentifier for hacku",
}

bdist_dmg_options = {
    "volume_label": "AudioIdentifier Installer",
    "applications_shortcut": False,
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="AudioIdentifier for hacku",
    version="1.0.0",
    description="Acoustic event identifier working with machine learning for HACK U",
    options={"build_exe": build_exe_options, "bdist_mac": bdist_mac_options, "bdist_dmg": bdist_dmg_options},
    executables=[Executable("main.py",
                            # icon="resource/icon.ico",
                            base=base,
                            shortcut_name="AudioIdentifier",
                            # shortcut_dir="DesktopFolder"
                            )],
)
