""" File and directory management """
# pylint: disable=broad-exception-caught

import os
import shutil
import json


EXT_IMG = [".png", ".jpeg", ".jpg"]


def create_folder(folder_path: str):
    """ Make folder if not exist """

    try:
        if not os.path.exists(folder_path):
            print(f"Making \"{folder_path}\" folder...")
            os.mkdir(folder_path)

            print("New folder created.")
            return json.dumps({
                "status": 201,
                "message": "Folder created.",
            })
        else:
            print(f"Folder \"{folder_path}\" exists.")
            return json.dumps({
                "status": 204,
                "message": "Folder exists.",
            })
    except Exception as e:
        print(f"Error creating folder \"{folder_path}\": {e}.")
        return json.dumps({
            "status": 500,
            "message": "Server error when creating a new folder.",
            "error": e
        })


def get_file_path(folder_path: str, file: str) -> str:
    """Get relative file path and return JSON string"""

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return json.dumps({
            "status": 404,
            "message": "Folder not found."
        })

    try:
        full_path = os.path.join(folder_path, file)

        if not os.path.exists(full_path):
            print(f"\"{file}\" not found in \"{folder_path}\".")
            return json.dumps({
                "status": 404,
                "message": "File not found."
            })
        else:
            print(f"Getting file location of: {file} in {folder_path}.")
            return json.dumps({
                "status": 200,
                "message": "Success getting file.",
                "path": full_path
            })
    except Exception as e:
        print(f"Error getting \"{file}\" in \"{folder_path}\": {e}.")
        return json.dumps({
            "status": 500,
            "message": "Server error when searching file.",
            "error": e
        })


def get_image_count(folder_path: str) -> int:
    """ Get image file count in a folder """

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return json.dumps({
            "status": 404,
            "message": "Folder not found."
        })

    try:
        file_count = len([
            file for file in os.listdir(folder_path)
            if any(file.lower().endswith(ext) for ext in EXT_IMG)
        ])

        print(f"Image count in \"{folder_path}\": {file_count}.")
        return json.dumps({
            "status": 200,
            "message": "Success getting file count.",
            "file_count": file_count
        })
    except Exception as e:
        print(f"Error counting image in \"{folder_path}\": {e}.")
        return json.dumps({
            "status": 500,
            "message": "Server error when searching file.",
            "error": e
        })


def move_file(file: str, current_folder: str, destination_folder: str):
    """ Move a file to another location """

    if not os.path.exists(current_folder):
        print(f"Folder {current_folder} not found.")
        return json.dumps({
            "status": 404,
            "message": "Folder not found.",
        })

    try:
        create_folder(destination_folder)

        src = os.path.join(current_folder, file)
        dst = os.path.join(destination_folder, file)

        if not os.path.exists(src):
            print(f"\"{file}\" not found in \"{current_folder}\".")
            return json.dumps({
                "status": 404,
                "message": "File not found."
            })
        else:
            shutil.move(src, dst)
            print(f"File moved from {src} to {dst}")
            return json.dumps({
                "status": 200,
                "message": "File moved."
            })
    except Exception as e:
        print(f"Error counting image in \"{current_folder}\": {e}.")
        return json.dumps({
            "status": 500,
            "message": "Server error when searching file.",
            "error": e
        })


def copy_file(file: str, current_folder: str, destination_folder: str):
    """ Copy file to another location """

    if not os.path.exists(current_folder):
        print(f"Folder {current_folder} not found.")
        return json.dumps({
            "status": 404,
            "message": "Folder not found.",
        })

    try:
        create_folder(destination_folder)

        src = os.path.join(current_folder, file)
        dst = os.path.join(destination_folder, file)

        if not os.path.exists(src):
            print(f"\"{file}\" not found in \"{current_folder}\".")
            return json.dumps({
                "status": 404,
                "message": "File not found."
            })
        else:
            shutil.copyfile(src, dst)
            print(f"File copied from {src} to {dst}...")
            return json.dumps({
                "status": 200,
                "message": "File copied."
            })
    except Exception as e:
        print(f"Error copying file \"{file}\" in \"{current_folder}\": {e}.")
        return json.dumps({
            "status": 500,
            "message": "Server error when copying file.",
            "error": e
        })


def get_last_file(folder_path: str):
    """ Get last added file according to time """

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return json.dumps({
            "status": 404,
            "message": "Folder not found.",
        })

    most_recent_file = None
    most_recent_time = 0

    try:
        for entry in os.scandir(folder_path):
            if entry.is_file():
                mod_time = entry.stat().st_mtime_ns
                if mod_time > most_recent_time:
                    most_recent_file = entry.name
                    most_recent_time = mod_time

        print(f"Got most recent file: {most_recent_file}")
        return json.dumps({
            "status": 200,
            "message": "Most recent file file searched and got.",
            "most_recent_file": most_recent_file
        })
    except Exception as e:
        print(f"Error searching last file in \"{folder_path}\": {e}.")
        return json.dumps({
            "status": 500,
            "message": "Server error when searching last file.",
            "error": e
        })


def empty_folder(folder_path: str):
    """ Empty folder """

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return json.dumps({
            "status": 404,
            "message": "Folder not found.",
        })

    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    except Exception as e:
        print(f"Error deleting files in \"{folder_path}\": {e}.")
        return json.dumps({
            "status": 500,
            "message": "Server error when deleting files.",
            "error": e
        })
