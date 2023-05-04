import shutil
from pathlib import Path

import nox
import os
import subprocess
import time
from signal import SIGKILL

DIR = Path(__file__).parent.resolve()


@nox.session(python=["python3.11"])
def build(session: nox.Session) -> None:
    """Build the dist."""
    dist_path = DIR.joinpath("dist")
    if dist_path.exists():
        shutil.rmtree(dist_path)

    session.install("poetry")
    session.run("poetry", "build")


@nox.session(python=["python3.11"])
def tests(session: nox.Session) -> None:
    """Run the tests."""
    session.install("-r", "requirements.txt")
    session.install('pytest')
    session.install("pytest-asyncio")
    session.env["PYTHONPATH"] = "src"

    # run the server
    process = subprocess.Popen(['uvicorn src.main:app'], shell=True)
    print(f"webserver process id: {process.pid}")

    try:
        # wait for the server to startup
        time.sleep(5)

        # run the integration tests
        session.run("pytest", "-p", "pytest_asyncio", "--asyncio-mode=auto")
    finally:
        # close the server process
        os.kill(process.pid, SIGKILL)


@nox.session(python=["python3.11"])
def lint(session: nox.Session) -> None:
    """Run the linter checks."""
    session.install('flake8')
    session.install("-r", "requirements.txt")

    # lint the source code
    session.run(
        'flake8', 'src',
        '--docstring-convention', 'google',
        '--ignore=D100'
    )

    # lint the tests
    session.run(
        'flake8', 'tests',
        '--docstring-convention', 'google',
        '--ignore=D100,D104'
    )
