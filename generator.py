"""Regenerates the index based on the specified folders.
"""
from typing import Final, Sequence

import hashlib
import pathlib
import re
import sys

HTML_HEADER: Final[str] = """\
<!DOCTYPE HTML>
<html>
    <head>
        <title>{Title}</title>
        <meta charset="UTF-8" />
    </head>

    <body>
    <h1>{Title}</h1>
"""
"""The header for a html page.

It contains the opening `<body>` tag and has the `Titel` interpolation.
"""

HTML_FOOTER: Final[str] = """\
    </body>
</html>
"""
"""Contains the footer of an html page.

This includes the closing `</body>` tag.
"""

def normalize_name(name: str) -> bool:
    """Normalize the project name according to the rules in PEP503."""
    return re.sub(r"[-_.]+", "-", name).lower()


def write_project_index(
        base_folder: pathlib.Path,
        project_name: str,
) -> int:
    # Project folder must exists because we assume that the files are located inside.
    project_folder = base_folder / project_name
    if not project_folder.is_dir():
        raise NotADirectoryError(
                f"Expected that the project folder `{project_folder}` for project `{project_name}` exists."
    )

    found_packages = 0
    normalized_project_name = normalize_name(project_name)
    with open(project_folder / "index.html", "wt") as index:
        index.write(HTML_HEADER.format(Title=f"Custom Package for '{project_name}'"))

        for file in project_folder.iterdir():
            filename = file.name
            if filename.startswith("."):
                continue
            elif not any(filename.endswith(ext) for ext in [".zip", ".tar.gz", ".whl"]):
                continue
            assert filename.startswith(normalized_project_name + "-")

            # Compute the hash such that we can append it to the link.
            with open(file, "rb") as F:
                digest = hashlib.file_digest(F, "sha256")

            # PEP503 says that the text of the anchor element must be the filename, so there
            #  is not need for fancy processing of the file name. Furthermore, we assume that
            #  the file names have the correct normalized name and version.
            index.write(
                    f'\t\t<a href="{filename}#sha256={digest.hexdigest()}">{filename}</a> </br>\n'.replace("\t", "    ")
            )
            found_packages += 1
        index.write(HTML_FOOTER)

        return found_packages


def write_package_index(
        base_folder: pathlib.Path,
        packages: Sequence[str],
) -> None:

    with open(base_folder / "index.html", "wt") as index:
        index.write(HTML_HEADER.format(Title=f"Custom Package Index for GT4Py"))

        for project_name in packages:
            project_folder = base_folder / project_name
            normalized_project_name = normalize_name(project_name)
            if not project_folder.is_dir():
                print(
                        f"There is not folder associated to the project `{project_name}`, skipping it.",
                        flush=True,
                        file=sys.stderr,
                )
                continue

            # Now generate the index for that file.
            found_packages = write_project_index(base_folder, project_name)

            if found_packages == 0:
                # Consider no packages not as an error, only output a warning.
                # TODO: Consider removing the folder.
                print(
                        f"No packages for project `{project_name}` could be located.",
                        flush=True,
                        file=sys.stderr,
                )
                continue

            index.write(f'\t\t<a href="{project_name}">{normalized_project_name}</a>\n'.replace("\t", "    "))

        index.write(HTML_FOOTER)


if __name__ == "__main__":
    write_package_index(
            base_folder=pathlib.Path(__file__).parent,
            packages=["dace", "ghex"],
    )
