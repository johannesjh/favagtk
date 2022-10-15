#!/usr/bin/env python3

import argparse
import json
import logging
import pathlib
import platform
import re
import shelve
import sys
import urllib.request
from contextlib import nullcontext, suppress
from dataclasses import asdict, dataclass, field
from functools import cached_property
from itertools import product
from typing import FrozenSet, Hashable, Iterable, Iterator, List, Optional, Tuple, Union

import pkg_resources

logger = logging.getLogger(__name__)


# =============================================================================
# Helper functions / semi vendored code
# =============================================================================

try:
    # use packaging.tags functionality if available
    from packaging.utils import parse_wheel_filename

    def tags_from_wheel_filename(filename: str) -> list[str]:
        _, _, _, tags = parse_wheel_filename(filename)
        return [str(tag) for tag in tags]

except ModuleNotFoundError:
    # fall back to a local implementation
    # that is heavily inspired by / almost vendored from the `packaging` package:
    def tags_from_wheel_filename(filename: str) -> list[str]:
        InvalidWheelFilename = Exception
        Tag = lambda *args: tuple(args)

        # the following code is based on packaging.tags.parse_tag,
        # it is needed for the parse_wheel_filename function:
        def parse_tag(tag: str) -> FrozenSet[Tag]:
            tags = set()
            interpreters, abis, platforms = tag.split("-")
            for interpreter in interpreters.split("."):
                for abi in abis.split("."):
                    for platform_ in platforms.split("."):
                        tags.add(Tag(interpreter, abi, platform_))
            return frozenset(tags)

        # the following code is based on packaging.utils.parse_wheel_filename:
        def parse_wheel_filename(wheel_filename: str) -> list[tuple]:
            if not wheel_filename.endswith(".whl"):
                raise InvalidWheelFilename(
                    f"Error parsing wheel filename: Invalid wheel filename (extension must be '.whl'): {wheel_filename}"
                )
            wheel_filename = wheel_filename[:-4]
            dashes = wheel_filename.count("-")
            if dashes not in (4, 5):
                raise InvalidWheelFilename(
                    f"Error parsing wheel filename: Invalid wheel filename (wrong number of parts): {wheel_filename}"
                )
            parts = wheel_filename.split("-", dashes - 2)
            return parse_tag(parts[-1])

        return ["-".join(tag_tuple) for tag_tuple in parse_wheel_filename(filename)]


# =============================================================================
# Data Structures
# =============================================================================


@dataclass(frozen=True, kw_only=True)
class Platform:
    python_version: list[str]
    python_tags: list[str]


@dataclass(frozen=True, kw_only=True)
class Requirement:
    package: str
    version: str


@dataclass(frozen=True, kw_only=True)
class Download:
    filename: str
    url: str
    sha256: str

    @cached_property
    def is_wheel(self):
        return self.filename.endswith(".whl")

    @cached_property
    def is_sdist(self):
        return not self.is_wheel and not self.filename.endswith(".egg")

    @cached_property
    def tags(self) -> list[str]:
        """Returns a list of tags that this download is compatible for"""
        # https://packaging.pypa.io/en/latest/utils.html#packaging.utils.parse_wheel_filename
        # https://packaging.pypa.io/en/latest/utils.html#packaging.utils.parse_sdist_filename
        if self.is_sdist:
            return []
        if self.filename.endswith(".whl"):
            return tags_from_wheel_filename(self.filename)

    @cached_property
    def arch(self) -> Optional[str]:
        """Returns a wheel's target architecture, and None for sdists."""
        if self.is_sdist:
            return None
        elif self.is_wheel:
            if any([tag.endswith("x86_64") for tag in self.tags]):
                return "x86_64"
            if any([tag.endswith("aarch64") for tag in self.tags]):
                return "aarch64"


@dataclass(frozen=True, kw_only=True)
class Release(Requirement):
    package: str
    version: str
    downloads: List[Download] = field(default_factory=list)


# =============================================================================
# Operations
# =============================================================================


class PlatformFactory:
    """Provides methods for creating platform objects."""

    @staticmethod
    def from_current_interpreter() -> Platform:
        """Returns a platform object that describes the current python interpreter and system."""

        def get_python_version() -> list[str]:
            return list(platform.python_version_tuple())

        def get_python_tags() -> Optional[list[str]]:
            try:
                import packaging.tags

                tags = [str(tag) for tag in packaging.tags.sys_tags()]
            except Exception as e:
                logger.warning(
                    "Python platform tags could not be determined.", exc_info=e
                )
                return None
            return tags

        return Platform(
            python_version=get_python_version(), python_tags=get_python_tags()
        )

    @classmethod
    def from_string(cls, platform_string: str):
        """
        Returns a platform object by parsing a platform string like '39-x86_64'.
        The string format is "{major}{minor}-{platform.machine}"
        """
        try:
            major, minor, arch = re.match(
                r"^(?:py|cp)?(\d)(\d+)-(.*)$", platform_string
            ).groups()
            return cls.from_python_version_and_arch(minor_version=int(minor), arch=arch)
        except AttributeError as e:
            logger.warning(f"Could not parse platform string {platform_string}")

    @staticmethod
    def from_python_version_and_arch(minor_version=None, arch="x86_64"):
        """
        Returns a platform object that roughly describes a cpython installation on linux.

        The tags in the platform object are a rough approximation, trying to match what
        `packaging.tags.sys_tags` would return if invoked on a linux system with cpython.

        Arguments:
        * minor_version: the python 3 minor version
        * arch: either "x86_64" or "aarch64"
        """
        assert minor_version is not None
        assert arch in ["x86_64", "aarch64"]

        def seq(start: int, end: int) -> Iterable[int]:
            """Returns a range of numbers, from start to end, in steps of +/- 1."""
            step = 1 if start < end else -1
            return range(start, end + step, step)

        def tags():
            cache = set()

            def dedup(obj: Hashable):
                if obj in cache:
                    return
                else:
                    cache.add(obj)
                    return obj

            platforms = [f"manylinux_2_{v}" for v in seq(35, 17)] + ["manylinux2014"]
            if arch == "x86_64":
                platforms += (
                    [f"manylinux_2_{v}" for v in seq(16, 12)]
                    + ["manylinux2010"]
                    + [f"manylinux_2_{v}" for v in seq(11, 5)]
                    + ["manylinux1"]
                )
            platforms += ["linux"]
            platform_tags = [f"{platform}_{arch}" for platform in platforms]

            # current cpython version, all abis, all platforms:
            for py in [f"cp3{minor_version}"]:
                for abi in [f"cp3{minor_version}", "abi3", "none"]:
                    for platform in platform_tags:
                        yield dedup(f"{py}-{abi}-{platform}")

            # older cpython versions, abi3, all platforms:
            for py in [f"cp3{v}" for v in seq(minor_version - 1, 2)]:
                for abi in ["abi3"]:
                    for platform in platform_tags:
                        yield dedup(f"{py}-{abi}-{platform}")

            # current python version, abi=none, all platforms:
            for py in [f"py3{minor_version}"]:
                for abi in ["none"]:
                    for platform in platform_tags:
                        yield dedup(f"{py}-{abi}-{platform}")

            # current major python version (py3), abi=none, all platforms:
            for py in ["py3"]:
                for abi in ["none"]:
                    for platform in platform_tags:
                        yield dedup(f"{py}-{abi}-{platform}")

            # older python versions, abi=none, all platforms:
            for py in [f"py3{v}" for v in seq(minor_version - 1, 0)]:
                for abi in ["none"]:
                    for platform in platform_tags:
                        yield dedup(f"{py}-{abi}-{platform}")

            # current python version, abi=none, platform=any
            yield f"py3{minor_version}-none-any"

            # current major python version, abi=none, platform=any
            yield "py3-none-any"

            # older python versions, abi=none, platform=any
            for py in [f"py3{v}" for v in seq(minor_version - 1, 0)]:
                yield f"{py}-none-any"

        return Platform(
            python_version=["3", str(minor_version)], python_tags=list(tags())
        )


class RequirementsParser:
    """
    Parses requirements.txt files in a very simple way:
    It expects all versions to be pinned.
    And it does not resolve dependencies.
    """

    # based on: https://stackoverflow.com/a/59971236
    # using functionality from pkg_resources.parse_requirements

    @classmethod
    def parse_string(cls, requirements_txt: str) -> List[Requirement]:
        """Parses requirements.txt string content into a list of Release objects."""

        def validate_requirement(req: pkg_resources.Requirement) -> None:
            assert (
                len(req.specs) == 1
            ), "Error parsing requirements: A single version numer must be specified."
            assert (
                req.specs[0][0] == "=="
            ), "Error parsing requirements: The exact version must specified as 'package==version'."

        def make_requirement(req: pkg_resources.Requirement) -> Requirement:
            validate_requirement(req)
            return Requirement(package=req.project_name, version=req.specs[0][1])

        reqs = pkg_resources.parse_requirements(requirements_txt)
        return [make_requirement(req) for req in reqs]

    @classmethod
    def parse_file(cls, file) -> List[Requirement]:
        """Parses a requirements.txt file into a list of Release objects."""
        if hasattr(file, "read"):
            req_txt = file.read()
        else:
            req_txt = pathlib.Path(file).read_text()
        return cls.parse_string(req_txt)


# Cache typealias
# This is meant for caching responses when querying package information.
# A cache can either be a dict for in-memory caching, or a shelve.Shelf
Cache = Union[dict, shelve.Shelf]  # type: TypeAlias


class PypiClient:
    """Provides methods for querying package information from the PyPi package index."""

    _cache: Cache = {}

    @property
    def cache(self) -> Cache:
        return type(self)._cache

    @cache.setter
    def cache(self, val: Cache):
        type(self)._cache = val

    @classmethod
    def _query(cls, url) -> str:
        def _query_from_cache(url) -> Optional[str]:
            try:
                return cls.cache[url]
            except KeyError:
                return None

        def _query_from_pypi(url) -> str:
            json_string = urllib.request.urlopen(url).read().decode("utf-8")
            cls.cache[url] = json_string
            return json_string

        return _query_from_cache(url) or _query_from_pypi(url)

    @classmethod
    def get_release(cls, req: Requirement) -> Release:
        """Queries pypi regarding available downloads for this requirement. Returns a release object."""
        url = f"https://pypi.org/pypi/{req.package}/{req.version}/json"
        json_string = cls._query(url)
        json_dict = json.loads(json_string)
        return Release(
            package=req.package,
            version=req.version,
            downloads=[
                Download(
                    filename=url["filename"],
                    url=url["url"],
                    sha256=url["digests"]["sha256"],
                )
                for url in json_dict["urls"]
            ],
        )

    @classmethod
    def get_releases(cls, reqs: Iterable[Requirement]) -> List[Release]:
        """Queries release information from a package index."""
        return [cls.get_release(req) for req in reqs]


class DownloadChooser:
    """
    Provides methods for choosing package downloads for installing a specific package release
    on a specific target platform.
    """

    @classmethod
    def matches(cls, download: Download, platform_tag: str) -> bool:
        """Returns True if the tags encoded in the download's filename match a target platform tag."""
        if download.is_sdist:
            return True

        return platform_tag in download.tags

    @classmethod
    def downloads(
        cls,
        release: Release,
        platform: Platform,
        wheels_only=False,
        sdists_only=False,
    ) -> Iterator[Download]:
        """
        Yields suitable downloads for a specific platform.
        The order of downloads matches the order of platform tags,
        i.e., preferred downloads are returned first.
        """
        cache = set()
        for (platform_tag, download) in product(
            platform.python_tags, release.downloads
        ):
            if download in cache:
                continue
            if wheels_only and not download.is_wheel:
                continue
            if sdists_only and not download.is_sdist:
                continue
            if cls.matches(download, platform_tag):
                cache.add(download)
                yield download

    @classmethod
    def wheel(
        cls,
        release: Release,
        platform: Platform,
    ) -> Optional[Download]:
        """Returns the preferred wheel download for this release, for a specific python platform"""
        try:
            return next(cls.downloads(release, platform, wheels_only=True))
        except StopIteration:
            return None

    @classmethod
    def sdist(cls, release: Release) -> Optional[Download]:
        """Returns the source package download for this release"""
        try:
            return next(filter(lambda d: d.is_sdist, release.downloads))
        except StopIteration:
            return None

    @classmethod
    def wheel_or_sdist(cls, release: Release, platform: Platform):
        """Returns a wheel or an sdist for this release, in this order of preference."""
        return cls.wheel(release, platform) or cls.sdist(release)

    @classmethod
    def sdist_or_wheel(cls, release: Release, platform: Platform):
        """Returns an sdist or a wheel for this release, in this order of preference."""
        return cls.sdist(release) or cls.wheel(release, platform)


class FlatpakGenerator:
    """Provides methods for generating a flatpak-builder build manifest."""

    @staticmethod
    def manifest(
        requirements: Iterable[Requirement],
        downloads: Iterable[Download],
        module_name="python3-package-installation",
        pip_install_template: str = 'pip3 install --verbose --exists-action=i --no-index --find-links="file://${PWD}" --prefix=${FLATPAK_DEST} --no-build-isolation ',
    ):
        def source(download: Download) -> dict:
            source = {"type": "file", "url": download.url, "sha256": download.sha256}
            if download.arch:
                source["only-arches"] = [download.arch]
            return source

        return {
            "name": module_name,
            "buildsystem": "simple",
            "build-commands": [
                pip_install_template + " ".join([req.package for req in requirements])
            ],
            "sources": [source(download) for download in downloads],
        }


# =============================================================================
# CLI commandline interface
# =============================================================================


def main():
    """ "
    The req2flatpak script generates a flatpak build manifest from python requirements.
    It comes with a simple commandline interface for basic usage.
    Advanced usage and customizations/tweaks are possible by invoking the script
    through its python API.
    """

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "--requirements",
        nargs="*",
        help="One or more requirements can be specified as commandline arguments, e.g., 'pandas==1.4.4'.",
    )
    parser.add_argument(
        "--requirements-file",
        "-r",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Requirements can be read from a specified requirements.txt file or from stdin.",
    )
    parser.add_argument(
        "--target-platforms",
        "-t",
        nargs="+",
        help="Target platforms can be specified as, e.g., '39-x86_64' or '310-aarch64'.",
    )
    parser.add_argument(
        "--cache",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Uses a persistent cache when querying pypi.",
    )
    parser.add_argument(
        "--outfile",
        "-o",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    parser.add_argument(
        "--platform-info",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Prints information about the current platform.",
    )
    parser.add_argument(
        "--installed-packages",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Prints installed packages in requirements.txt format.",
    )

    # parse commandline arguments
    options = parser.parse_args()

    # print platform info if requested, and exit
    if options.platform_info:
        output_stream = (
            options.outfile if hasattr(options.outfile, "write") else sys.stdout
        )
        platform = PlatformFactory.from_current_interpreter()
        json.dump(asdict(platform), output_stream, indent=4)
        parser.exit()

    # print installed packages if requested, and exit
    if options.installed_packages:
        output_stream = (
            options.outfile if hasattr(options.outfile, "write") else sys.stdout
        )
        try:
            import pkg_resources

            pkgs = {p.key: p.version for p in pkg_resources.working_set}
            for pkg, version in pkgs.items():
                print(f"{pkg}=={version}", file=output_stream)
        except Exception as e:
            logger.warning("Could not determine installed python packages.", exc_info=e)
            return None
        finally:
            parser.exit()

    # parse requirements
    requirements = []
    with suppress(AttributeError):
        if reqs := options.requirements:
            requirements += RequirementsParser.parse_string("\n".join(reqs))
        if reqs := options.requirements_file:
            requirements += RequirementsParser.parse_file(reqs)
    if not len(requirements):
        parser.error(
            "Error parsing requirements. At least one requirement must be specified."
        )

    # parse target platforms
    if not options.target_platforms:
        parser.error(
            "Error parsing target platforms. Missing commandline argument, at least one target platform must be specified as, e.g., '39-x86_64' or '310-aarch64'."
        )
    platforms = [
        PlatformFactory.from_string(platform) for platform in options.target_platforms
    ]
    if not len(platforms):
        parser.error(
            "Error parsing target platforms. At least one target platform must be specified as, e.g., '39-x86_64' or '310-aarch64'."
        )

    # query released downloads from PyPi, optionally using a shelve.Shelf to cache responses:
    with shelve.open("../pypi_cache") if options.cache else nullcontext() as cache:
        PypiClient.cache = cache or {}
        releases = PypiClient.get_releases(requirements)

    # choose suitable downloads for the target platforms
    downloads = {
        DownloadChooser.wheel_or_sdist(release, platform)
        for release in releases
        for platform in platforms
    }

    # generate flatpak build manifest
    manifest = FlatpakGenerator.manifest(requirements, downloads)

    # write output
    output_stream = options.outfile if hasattr(options.outfile, "write") else sys.stdout
    json.dump(manifest, output_stream, indent=4)


if __name__ == "__main__":
    main()
