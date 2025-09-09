#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Richard Majewski <uglyegg@entropy.quest>
#
# SPDX-License-Identifier: GPL-3.0-only

"""
A command-line tool for managing SPDX headers in Python source files.

This script can add, remove, change, or verify SPDX headers in all Python files
within the repository's source directory.

Options:
  -a, --add <LICENSE>     Add an SPDX header for a specified license.
  -r, --remove            Remove any existing SPDX header.
  -c, --change <LICENSE>  Change an existing SPDX header to a new license.
  -v, --verify            Verify that all Python files have a valid SPDX header.
  -l, --list              List available license keywords.
"""

import argparse
import datetime
import os
import tomllib
from pathlib import Path

# Global variables for copyright information.
COPYRIGHT_YEAR = str(datetime.date.today().year)

# Load author info from pyproject.toml
pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
with open(pyproject_path, "rb") as f:
    pyproject_data = tomllib.load(f)
project_authors = pyproject_data.get("project", {}).get("authors", [])
if project_authors:
    COPYRIGHT_NAME = project_authors[0].get("name", "John Doe")
    COPYRIGHT_EMAIL = project_authors[0].get("email", "jdoe@geocities.com")
else:
    COPYRIGHT_NAME = "John Doe"
    COPYRIGHT_EMAIL = "jdoe@geocities.com"


# Define the supported licenses and their corresponding headers.
# The keys are the command-line keywords (e.g., 'GPL', 'MIT').
# The 'header' value contains the full SPDX comment block.
def create_header(identifier, year, name, email):
    """Generates the SPDX header string for a given license identifier."""
    return f"""# SPDX-FileCopyrightText: {year} {name} <{email}>
#
# SPDX-License-Identifier: {identifier}

"""


LICENSES = {
    "GPL-2.0": {"identifier": "GPL-2.0-only"},
    "GPL-3.0": {"identifier": "GPL-3.0-only"},
    "AGPL-3.0": {"identifier": "AGPL-3.0-only"},
    "LGPL-2.1": {"identifier": "LGPL-2.1-only"},
    "LGPL-3.0": {"identifier": "LGPL-3.0-only"},
    "MIT": {"identifier": "MIT"},
    "Apache-2.0": {"identifier": "Apache-2.0"},
    "BSD-2-Clause": {"identifier": "BSD-2-Clause"},
    "BSD-3-Clause": {"identifier": "BSD-3-Clause"},
    "ISC": {"identifier": "ISC"},
    "MPL-2.0": {"identifier": "MPL-2.0"},
    "Unlicense": {"identifier": "Unlicense"},
    "CC0-1.0": {"identifier": "CC0-1.0"},
    "EPL-2.0": {"identifier": "EPL-2.0"},
    "CDDL-1.0": {"identifier": "CDDL-1.0"},
}

# Pre-generate the full header text for each license
for key, value in LICENSES.items():
    value["header"] = create_header(
        value["identifier"], COPYRIGHT_YEAR, COPYRIGHT_NAME, COPYRIGHT_EMAIL
    )


def add_header_to_py_files(directory, license_keyword):
    """
    Recursively finds all .py files in a directory and adds the SPDX header
    for the specified license if it's not already present.
    """
    if license_keyword not in LICENSES:
        print(
            f"Error: License keyword '{license_keyword}' is not supported. Use -l to list available licenses."
        )
        return

    header_to_add = LICENSES[license_keyword]["header"]

    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        lines = f.readlines()

                    # Check for an existing header to avoid duplicates.
                    if any("SPDX-FileCopyrightText" in line for line in lines):
                        print(
                            f"File '{filepath}' already has an SPDX header. Skipping."
                        )
                        continue

                    # Check for a shebang line
                    shebang = ""
                    if lines and lines[0].startswith("#!"):
                        shebang = lines.pop(0)

                    # Prepend the new header to the existing content.
                    new_lines = []
                    if shebang:
                        new_lines.append(shebang)
                    new_lines.extend(header_to_add.splitlines(keepends=True))
                    new_lines.extend(lines)

                    # Write the new content back to the file.
                    with open(filepath, "w") as f:
                        f.writelines(new_lines)
                    print(f"Successfully added header to '{filepath}'")

                except IOError as e:
                    print(f"Error processing file '{filepath}': {e}")


def remove_header_from_py_files(directory):
    """
    Recursively finds all .py files in a directory and removes an SPDX header
    if it exists.
    """
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        lines = f.readlines()

                    if not any("SPDX-FileCopyrightText" in line for line in lines):
                        print(
                            f"File '{filepath}' does not have an SPDX header. Skipping."
                        )
                        continue

                    new_lines = []
                    in_header = False
                    for line in lines:
                        if "SPDX-FileCopyrightText" in line:
                            in_header = True
                            continue

                        if in_header and not line.strip().startswith("#"):
                            # End of header block, so stop removing lines.
                            in_header = False

                        if not in_header:
                            new_lines.append(line)

                    # Write the modified content back to the file.
                    with open(filepath, "w") as f:
                        f.writelines(new_lines)
                    print(f"Successfully removed header from '{filepath}'")

                except IOError as e:
                    print(f"Error processing file '{filepath}': {e}")


def change_header_in_py_files(directory, license_keyword):
    """
    Recursively finds all .py files with an SPDX header and changes the
    license identifier to the specified new license.
    """
    if license_keyword not in LICENSES:
        print(
            f"Error: License keyword '{license_keyword}' is not supported. Use -l to list available licenses."
        )
        return

    new_identifier = LICENSES[license_keyword]["identifier"]

    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        lines = f.readlines()

                    found_header = False
                    found_identifier = False
                    new_lines = []

                    for line in lines:
                        if "SPDX-FileCopyrightText" in line:
                            found_header = True

                        if "SPDX-License-Identifier" in line:
                            new_lines.append(
                                f"# SPDX-License-Identifier: {new_identifier}\n"
                            )
                            found_identifier = True
                        else:
                            new_lines.append(line)

                    if not found_header:
                        print(
                            f"File '{filepath}' does not have an SPDX header. Skipping."
                        )
                        continue

                    if not found_identifier:
                        print(
                            f"File '{filepath}' has a copyright text but no license identifier. Skipping."
                        )
                        continue

                    # Write the modified content back to the file.
                    with open(filepath, "w") as f:
                        f.writelines(new_lines)
                    print(
                        f"Successfully changed header in '{filepath}' to '{new_identifier}'"
                    )

                except IOError as e:
                    print(f"Error processing file '{filepath}': {e}")


def verify_spdx_headers(directory):
    """
    Recursively finds all .py files in a directory and verifies that they
    have a valid SPDX header.
    """
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    files_with_issues = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        content = f.read(256)  # Read a small chunk to check for header

                    if (
                        "SPDX-FileCopyrightText" not in content
                        or "SPDX-License-Identifier" not in content
                    ):
                        files_with_issues.append(filepath)

                except IOError as e:
                    print(f"Warning: Could not read file '{filepath}': {e}")

    if not files_with_issues:
        print("All Python files in the source directory have a valid SPDX header.")
    else:
        print("The following files are missing a valid SPDX header:")
        for file in files_with_issues:
            print(f"- {file}")


def main():
    """
    Main function to parse command-line arguments and call the appropriate function.
    """
    parser = argparse.ArgumentParser(
        description="A script to add, remove, or change SPDX headers from Python files.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-a",
        "--add",
        type=str,
        metavar="LICENSE",
        help="Add the SPDX header for the specified LICENSE to all Python files.",
    )
    group.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="Remove the SPDX header from all Python files.",
    )
    group.add_argument(
        "-c",
        "--change",
        type=str,
        metavar="LICENSE",
        help="Change the SPDX license identifier in all Python files to the specified LICENSE.",
    )
    group.add_argument(
        "-v",
        "--verify",
        action="store_true",
        help="Verify that all Python files have a valid SPDX header.",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List available license keywords."
    )

    args = parser.parse_args()

    # Get the directory of the script and then construct the path to the 'src' directory.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, "..", "src")

    if args.list:
        print("Available license keywords:")
        for license_name, details in LICENSES.items():
            print(f"- {license_name} (SPDX: {details['identifier']})")
    elif args.add:
        add_header_to_py_files(src_dir, args.add)
    elif args.remove:
        remove_header_from_py_files(src_dir)
    elif args.change:
        change_header_in_py_files(src_dir, args.change)
    elif args.verify:
        verify_spdx_headers(src_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
