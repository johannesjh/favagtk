#!/usr/bin/env python3
import argparse
import importlib.util
import logging
import subprocess
import venv
from pathlib import Path

from poetry.factory import Factory


class PoetryToVenv:
    """
    Helper class to create a python virtual environment for a given poetry project.
    It installs dependencies as specified in poetry's lock file, except for specific
    packages that are excluded in order to use them from the system's site packages.
    """

    def make_venv(self, poetry, venv_dir, excluded_package_names):
        logging.info(f"Creating virtual environment in {venv_dir}...")
        venv.create(
            env_dir=venv_dir, system_site_packages=True, clear=True, with_pip=True
        )

        logging.info("Assembling list of requirements...")
        pip_requirements = self.get_filtered_pip_requirements(
            poetry, exclude=excluded_package_names
        )

        # install requirements using pip install
        pip = str(Path(venv_dir) / "bin" / "pip")
        pip_cmd = [
            pip,
            "install",
            "--ignore-installed",
        ] + pip_requirements
        logging.info(f"Installing packages:\n{pip_cmd}")
        subprocess.check_call(pip_cmd)

    def get_filtered_pip_requirements(self, poetry, exclude=[]):
        """
        Returns filtered dependencies of the poetry project,
        in a format suited as arguments for calling "pip install".
        """
        # get list of filtered dependencies
        package = poetry.package
        locked_repo = poetry.locker.locked_repository(True)
        locked_packages = locked_repo.packages
        dependencies = self.get_filtered_dependencies(package, locked_packages, exclude)

        # formats dependencies for use with pip install,
        # code inspired by poetry.console.commands.export.ExportCommand
        pip_requirements = []
        for dependency in dependencies:
            requirement = dependency.to_pep_508(with_extras=False)
            is_direct_reference = (
                dependency.is_vcs()
                or dependency.is_url()
                or dependency.is_file()
                or dependency.is_directory()
            )
            if is_direct_reference:
                pip_requirements.append(requirement)
                continue
            req = f"{dependency.name}=={dependency.pretty_constraint}"
            if ";" in requirement:
                markers = requirement.split(";", 1)[1].strip()
                if markers:
                    req += f"; {markers}"
            pip_requirements.append(req)
        return pip_requirements

    def get_filtered_dependencies(
        self, package, locked_packages, exclude=[], result=set()
    ):
        """Returns filtered dependencies of the poetry package"""
        # code inspired by poetry.console.commands.show.ShowCommand.handle
        for required in package.requires:
            if required.name in exclude:
                continue
            for package in locked_packages:
                if package.name == required.name:
                    result.add(package.to_dependency())
                    self.get_filtered_dependencies(
                        package, locked_packages, exclude, result=result
                    )
        return result


class FavaGtkVenv:
    """
    Creates a python virtual environment for developing FavaGtk.
    Dependencies of FavaGtk are installed in the virtual environment,
    except for packages where it easier to use their system-wide installation.
    Specifically, PyGObject is not installed but used from the system-wide
    site-packages.
    """

    def main(self):
        self.parse_arguments()
        self.check_overwriting()
        self.check_site_packages()
        self.parse_poetry_project()
        return self.create_venv()

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-p",
            "--poetry-project",
            type=str,
            default=str(Path(__file__).resolve().parent),
            help="folder where the FavaGtk poetry project is located.",
        )
        parser.add_argument(
            "-d",
            "--venv-dir",
            type=str,
            default=str(Path(__file__).resolve().parent / "venv"),
            help="folder where the virtual environment shall be created",
        )
        parser.add_argument(
            "-s",
            "--site-packages",
            type=str,
            nargs="+",
            default=["pygobject"],
            help="These packages will not be installed in the virtual environment",
        )
        parser.add_argument("-o", "--overwrite", action="store_true", default=False)
        self.args = parser.parse_args()

    def check_overwriting(self):
        if Path(self.args.venv_dir).exists() and not self.args.overwrite:
            print(
                f"The virtualenv won't be created because "
                f"folder {self.args.venv_dir} exists already."
            )
            print("You can delete the virtualenv folder and run this command again.")
            print("Alternatively, you can run this command using the --overwrite flag.")
            exit(77)  # similar to EX_NOPERM in sysexit.h

    def check_site_packages(self):
        # based on: https://stackoverflow.com/a/41815890
        for package_name in self.args.site_packages:
            spec = importlib.util.find_spec(package_name)
            if spec is None:
                logging.warning(
                    f"Package {package_name} was not found. "
                    f"Make sure it is installed in your system-wide site_packages "
                    f"so that FavaGtk's virtual environment will be able to use it."
                )

    def parse_poetry_project(self):
        self.poetry = Factory().create_poetry(self.args.poetry_project)

    def create_venv(self):
        return PoetryToVenv().make_venv(
            self.poetry, self.args.venv_dir, self.args.site_packages
        )


if __name__ == "__main__":
    exit(FavaGtkVenv().main())
