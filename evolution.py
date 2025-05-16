import dataclasses
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

MAX_VERSION = 87


def download_releases(download: bool = True):
    releases = [f"1.{v}.0" for v in range(0, MAX_VERSION + 1)]

    for release in releases:
        print(f"Installing {release}")
        if download:
            subprocess.run(["rustup", "toolchain", "install", "--no-self-update", release],
                           stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
        yield release


def get_programs():
    dir = Path("programs")
    for path in os.listdir(dir):
        path = dir / path
        assert path.suffix == ".rs"
        yield path.absolute()


def get_output(args) -> str:
    (release, program) = args
    with open(program) as f:
        src = f.read()

    with tempfile.TemporaryDirectory() as tmpdir:
        output = subprocess.run(["rustc", f"+{release}",
                                 "--out-dir", tmpdir,
                                 "--color", "always", "-"],
                                input=src.encode("utf8"),
                                stderr=subprocess.PIPE)
    return output.stderr.decode("utf8").strip()


@dataclasses.dataclass
class ErrorVersion:
    release: str
    stderr: str


@dataclasses.dataclass
class Program:
    name: str
    source: str
    versions: List[ErrorVersion]


@dataclasses.dataclass
class Output:
    programs: List[Program]


if __name__ == "__main__":
    releases = list(download_releases(False))
    programs = list(get_programs())

    from multiprocessing.pool import ThreadPool as Pool

    program_results = []
    with Pool() as pool:
        for program in programs:
            versions = []

            args = [(release, program) for release in releases]
            for (stderr, (release, _)) in zip(pool.map(get_output, args), args):
                version = ErrorVersion(release=release, stderr=stderr)
                if len(versions) == 0 or versions[-1].stderr != version.stderr:
                    versions.append(version)
            print(f"Found {len(versions)} different version(s) for {program.stem}")
            with open(program) as f:
                src = f.read()
            program_results.append(Program(name=program.stem, source=src, versions=versions))
    with open("errors.json", "w") as f:
        f.write(
            json.dumps(dataclasses.asdict(Output(programs=program_results))))
