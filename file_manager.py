""" File and directory management """
# pylint: disable=broad-exception-caught

import os
import shutil


EXT_IMG = [".png", ".jpeg", ".jpg"]



def make_folder(folder_path: str):
    """ Make folder if not exist """

    if not os.path.exists(folder_path):
        print(f"Making \"{folder_path}\" folder...")
        os.mkdir(folder_path)
    else:
        print(f"Folder \"{folder_path}\" exists.")


def get_file_path(file_path: str, file_name: str) -> str:
    " Get relative file path "

    if os.path.exists(os.path.join(file_path, file_name)):
        print(f"Getting file location of: {file_name}")
        return os.path.join(file_path, file_name)

    print("File not found")
    return "File not found"


def get_image_count(folder_path: str) -> int:
    """ Get image file count in a folder """

    if os.path.exists(folder_path):
        return len([
            file for file in os.listdir(folder_path)
            if any(file.lower().endswith(ext) for ext in EXT_IMG)
        ])

    print("Path not found")
    return "Path not found"


def move_file(file: str, current_folder: str, destination_folder: str):
    """ Move file location """

    make_folder(destination_folder)

    src = os.path.join(current_folder, file)
    dst = os.path.join(destination_folder, file)

    print(f"Moving file from {src} to {dst}...")
    shutil.move(src, dst)


def copy_file(file: str, current_folder: str, destination_folder: str):
    """ Copy file """

    make_folder(destination_folder)

    src = os.path.join(current_folder, file)
    dst = os.path.join(destination_folder, file)

    print(f"Copying file from {src} to {dst}...")
    shutil.copyfile(src, dst)


def get_last_file(folder_path: str):
    """ Get last added file according to time """

    most_recent_file = None
    most_recent_time = 0

    if os.path.exists(folder_path):
        for entry in os.scandir(folder_path):
            if entry.is_file():
                mod_time = entry.stat().st_mtime_ns
                if mod_time > most_recent_time:
                    most_recent_file = entry.name
                    most_recent_time = mod_time

        print(f"Most recent file: {most_recent_file}")
        return most_recent_file

    print("Path not found")
    return "Path not found"


def empty_folder(folder_path: str):
    """ Empty folder """

    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    print("Path not found")
    return "Path not found"
