import tempfile

import nox
from nox.sessions import Session

locations = "src", "tests", "./noxfile.py"
nox.options.sessions = "lint", "mypy", "tests", "black"


@nox.session(python=["3.8", "3.11"])
def lint(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=["3.8", "3.11"])
def tests(session: Session) -> None:
    args = session.posargs or ["--cov", "-m", "not e2e"]
    # session.run("poetry", "install", "--no-dev", external=True)
    # session.run("poetry", "install", "--help", external=True)
    session.run("poetry", "install", "--only=main", external=True)
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


@nox.session(python="3.11")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.11")
def safety(session: Session) -> None:
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with=dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


def install_with_constraints(session: Session, *args: str, **kwargs: int) -> None:
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with=dev",
            "--format=constraints.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        # session.run("cat",f"{requirements.name}")
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.11"])
def mypy(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


package = "hypermodern_pc"


@nox.session(python=["3.8", "3.11"])
def typeguard(session: Session) -> None:
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--only=main", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)
