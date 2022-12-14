from pathlib import Path
from shutil import move, rmtree
from subprocess import check_call

from setuptools import setup


def build_gui():
    proj = Path(__file__).parent
    gui_proj = proj / "mvnb-gui"
    gui_dest = proj / "mvnb" / "gui"
    gui_dist = gui_proj / "dist"

    # build only when gui proj exists
    if not gui_proj.exists():
        return

    # yarn install
    check_call(["yarn", "install"], cwd=gui_proj)

    # yarn parcel build
    gui_dist.exists() and rmtree(gui_dist)
    check_call(["yarn", "build", "--no-source-maps"], cwd=gui_proj)

    # deploy gui source
    gui_dest.exists() and rmtree(gui_dest)
    move(gui_dist, gui_dest)


build_gui()

setup(
    name="mvnb",
    packages=["mvnb"],
    version="0.0.0",
    package_data={"mvnb": ["gui/**/*"]},
    install_requires=["tornado>=6.2.0"],
    entry_points=dict(console_scripts=["mvnb=mvnb.__main__:main"]),
)
