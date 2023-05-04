#!/usr/bin/env python3
"""Default: create wheel."""
import glob

import tomli
from doit.tools import create_folder

DOIT_CONFIG = {"default_tasks": ["all"]}


def dumpkeys(infile, table, outfile):
    """Dump TOML table keys one per line."""
    with open(infile, "rb") as fin:
        full = tomli.load(fin)
    with open(outfile, "w") as fout:
        print(*full[table], sep="\n", file=fout)


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
        "actions": ["git clean -xdf"],
    }


def task_html():
    """Make HTML documentationi."""
    return {
        "actions": ["sphinx-build -M html docs build"],
    }


def task_test():
    """Preform tests."""
    yield {"actions": ["coverage run -m unittest -v"], "name": "run"}
    yield {"actions": ["coverage report"], "verbosity": 2, "name": "report"}


def task_pot():
    """Re-create .pot ."""
    return {
        "actions": ["pybabel extract -o locale/client.pot Client"],
        "file_dep": glob.glob("Client/*.py"),
        "targets": ["locale/client.pot"],
    }


def task_po():
    """Update translations."""
    return {
        "actions": ["pybabel update -D checkers -d locale/. -i locale/client.pot"],
        "file_dep": ["locale/client.pot"],
        "targets": ["locale/ru/LC_MESSAGES/checkers.po"],
    }


def task_mo():
    """Compile translations."""
    return {
        "actions": [
            (create_folder, ["Client/ru/LC_MESSAGES"]),
            "pybabel compile -D checkers -l ru -i locale/ru/LC_MESSAGES/checkers.po -d Client",
        ],
        "file_dep": ["locale/ru/LC_MESSAGES/checkers.po"],
        "targets": ["Client/ru/LC_MESSAGES/checkers.mo"],
    }


def task_sdist():
    """Create source distribution."""
    return {
        "actions": ["python -m build -s -n"],
        "task_dep": ["gitclean"],
    }


def task_wheel():
    """Create binary wheel distribution."""
    return {
        "actions": ["python -m build -n -w"],
        "task_dep": ["mo", "requirements"],
    }


def task_app():
    """Run application."""
    import Client.client

    return {
        "actions": [Client.client.main],
        "task_dep": ["mo"],
    }


def task_style():
    """Check style against flake8."""
    return {"actions": ["flake8 ."]}


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {"actions": ["pydocstyle ."]}


def task_check():
    """Perform all checks."""
    return {"actions": None, "task_dep": ["style", "docstyle", "test"]}


def task_all():
    """Perform all build task."""
    return {"actions": None, "task_dep": ["check", "wheel", "html"]}


def task_buildreq():
    """Try to calculate build requirements."""
    return {"actions": ["python BuildReq.py doit all"], "task_dep": ["gitclean"]}


def task_requirements():
    """Dump Pipfile requirements."""
    return {
        "actions": [(dumpkeys, ["Pipfile", "packages", "requirements.txt"])],
        "file_dep": ["Pipfile"],
        "targets": ["requirements.txt"],
    }
