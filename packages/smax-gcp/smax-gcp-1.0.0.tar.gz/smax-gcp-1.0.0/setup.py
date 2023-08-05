import pathlib
import time
import os
import shutil
import pkg_resources
from setuptools import setup, find_packages
from distutils.dir_util import copy_tree

python_ver = "3.7"
version = "1.0.0"


def _search_projects(suite="*", platform="*"):
    def match(suite_, platform_):
        match_suite = True if suite == "*" else suite_ == suite
        match_platform = True if platform == "*" else platform_ == platform
        return match_suite and match_platform

    for suite_dir in pathlib.Path(".").iterdir():
        if (
            not "sharelib" == suite_dir.name.lower()
            and suite_dir.joinpath("__init__.py").exists()
        ):
            for platform_dir in suite_dir.iterdir():
                if (
                    not "sharelib" == suite_dir.name.lower()
                    and platform_dir.joinpath("__init__.py").exists()
                ):
                    if match(suite_dir.name, platform_dir.name):
                        yield (suite_dir, platform_dir)


def _setup(suite_dir, platform_dir):
    prj_name = f"{suite_dir.name}-{platform_dir.name}"
    prj_pkg = f"{suite_dir.name}.{platform_dir.name}"

    long_description = ""
    readme_path = platform_dir.joinpath("README.md")
    if readme_path.exists():
        with readme_path.open("r") as fh:
            long_description = fh.read()

    install_requires = set()

    def add_requires(requirements_path: pathlib.Path):
        if requirements_path.exists():
            with requirements_path.open("r") as fh:
                install_requires.update(
                    [
                        str(requirement)
                        for requirement in pkg_resources.parse_requirements(fh)
                    ]
                )

    add_requires(platform_dir.joinpath("requirements.txt"))
    add_requires(pathlib.Path("sharelib").joinpath("requirements.txt"))

    with pathlib.Path("MANIFEST.in").open("w") as f:
        # f.write("include LICENSE" + os.linesep)
        f.write(f"include  *.py" + os.linesep)
        f.write(
            f"recursive-include {str(suite_dir)} *.tf *.jinja2 *.json *.sh *.md *.txt *.config *.tpl *.conf"
            + os.linesep
        )

    tf_config_path = pathlib.Path("tfconfig").joinpath(platform_dir.name)
    shutil.rmtree(platform_dir.joinpath(".tfconfig"), ignore_errors=True)
    copy_tree(
        str(tf_config_path), str(platform_dir.joinpath(".tfconfig")), verbose=0
    )

    setup(
        name=prj_name,
        version=version,
        author="",
        author_email=" ",
        description="",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="",
        packages=find_packages(
            exclude=["ez_setup", "tests*"],
            include=[suite_dir.name, prj_pkg, "sharelib"],
        ),
        include_package_data=True,
        # package_data={prj_pkg: ['tfconfig/*', 'tfconfig/**/*', 'tfconfig/**/**/*', '*.txt']},
        # data_files=[('tf', ['tfconfig/**/*'])],
        install_requires=list(install_requires),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=f">={python_ver}",
        entry_points=f"""
           [console_scripts]
           {prj_name} = {prj_pkg}.main:main
        """,
    )
    pathlib.Path("MANIFEST.in").unlink()
    return prj_name


def main():
    suite = os.environ["BUILD_SUITE"] if "BUILD_SUITE" in os.environ else "*"
    suite = suite if suite else "*"
    platform = (
        os.environ["BUILD_PLATFORM"] if "BUILD_PLATFORM" in os.environ else "*"
    )
    platform = platform if platform else "*"
    build_projects = []
    for project in _search_projects(suite, platform):
        print(os.linesep, f"=== Project: {project[1]} ===", os.linesep)
        build_projects.append(_setup(*project))

    print(os.linesep, "*** Summary ***")
    for project in build_projects:
        print(f"Done: {project}")

    if len(build_projects) == 0:
        print(
            "No project found!",
            os.linesep,
            f"BUILD_SUITE={suite}",
            os.linesep,
            f"BUILD_PLATFORM={platform}",
        )


if __name__ == "__main__":
    main()
