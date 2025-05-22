#!/usr/bin/env python3

import itertools
import os
import subprocess


def find_name_pairs(directory):
    cpp_files = {}  # Map to store .cpp files.
    cfg_files = set()  # Set to store .cfg files.

    # Traverse through the files in the directory.
    with os.scandir(directory) as entries:
        files = [entry.name for entry in entries if entry.is_file()]
    for file in files:
        if file.endswith(".cpp"):
            name = file[:-4]
            cpp_files[name] = os.path.join(directory, file)
        elif file.endswith(".cfg"):
            name = file[:-4]
            cfg_files.add(name)

    # Find intersection of keys to get matching pairs.
    name_pairs = {name for name in cpp_files if name in cfg_files}
    pairs_with_defaults = [
        (cpp_files[name], os.path.join(directory, f"{name}.cfg")) for name in name_pairs
    ]

    # Add pairs using large.cpp as default for configs without cpp files.
    for cfg_name in cfg_files - name_pairs:
        pairs_with_defaults.append(
            ("large.cpp", os.path.join(directory, f"{cfg_name}.cfg"))
        )

    return pairs_with_defaults


def get_files_with_suffix(entries, suffix):
    return [entry.name for entry in entries if entry.name.endswith(suffix)]


def get_files(directory):
    with os.scandir(directory) as entries:
        entries_list = list(entries)  # Needed to interate twice.
        cfg_files = get_files_with_suffix(entries_list, ".cfg")
        cpp_files = get_files_with_suffix(entries_list, ".cpp")
    return cpp_files, cfg_files


def process_files(source, formatted):
    cpp_files, cfg_files = get_files(source)
    for cpp_file, cfg_file in itertools.product(cpp_files, cfg_files):
        cpp_name = cpp_file[:-4]
        cfg_name = cfg_file[:-4]
        output_name = f"{cpp_name}+{cfg_name}.cpp"
        cpp_path = os.path.join(source, cpp_file)
        cfg_path = os.path.join(source, cfg_file)
        output_path = os.path.join(formatted, output_name)
        command = ["uncrustify", "-c", cfg_path, "-f", cpp_path, "-o", output_path]
        if True:
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while processing {cpp_file}: {e}")
        else:
            #print(f'Formatting {cpp_path} with {cfg_path} to {output_path}')
            print(" ".join(command))


def get_directories(source):
    with os.scandir(source) as entries:
        directories = [entry.name for entry in entries if entry.is_dir()]
    return directories


def main():
    source_root = "source"
    formatted_root = "formatted"
    directories = get_directories(source_root)
    for directory in directories:
        source = os.path.join(source_root, directory)
        formatted = os.path.join(formatted_root, directory)
        process_files(source, formatted)


if __name__ == "__main__":
    main()
