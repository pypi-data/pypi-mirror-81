"""
Storing weights for pytorch models
"""

import os
import torch
from . import mount_drive


def get_path(model_name, gdrive):
    """
    Return's path for the given model_name
    """
    if gdrive is True:
        path = mount_drive.gdrive(model_name)
    else:
        path = os.path.join(model_name)

    return path


def get_file_names(path):
    """
    Return's file names inside the given path
    """

    if os.path.isdir(path):
        file_names = os.listdir(path)
        file_names.sort()
        if len(file_names) != 0:
            return file_names
    print("Previous checkpoint dosen't exist")
    return None


def get_last_version(file_names):
    """
    Return's the latest version stored as checkpoint
    """
    return int(file_names[-1].split("_v")[1].split(".tar")[0])


def view(model_name, gdrive=False):
    """
    Display all the version's for the given model_name.
    """

    path = get_path(model_name, gdrive)
    if path is not None:
        file_names = get_file_names(path)
        if file_names is not None:
            print(file_names)


def save(model_name, model, optimizer=None, extra_info=dict, gdrive=False):
    """
    Stores the checkpoint.
    """
    path = get_path(model_name, gdrive)
    if path is not None:
        if not os.path.isdir(path):
            print("Creating checkpoint directory as:", model_name)
            os.mkdir(path)
            version = 0

        else:
            file_names = get_file_names(path)
            if file_names is not None:
                version = get_last_version(file_names) + 1
            else:
                version = 0

        file_path = os.path.join(path, f"{model_name}_v{version}.tar")

        if optimizer is None:
            optimizer_state_dict = {}
        else:
            optimizer_state_dict = optimizer.state_dict()

        print(f"Saving Checkpoint: {model_name}_v{version}.tar")
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer_state_dict,
                "extra_info": extra_info,
            },
            file_path,
        )


def load(model_name, model, optimizer=None, version=None, return_extra_info=False, gdrive=False):  # pylint: disable=too-many-arguments
    """
    Load's the latest checkpoint.
    If version is provided than it ll load that perticular version.
    """

    path = get_path(model_name, gdrive)
    if path is not None:
        file_names = get_file_names(path)

        if file_names is not None:
            if version is None:
                version = get_last_version(file_names)

            file_path = os.path.join(path, f"{model_name}_v{version}.tar")

            if os.path.isfile(file_path):
                print(f"Loading Checkpoint: {model_name}_v{version}.tar")
                checkpoint = torch.load(file_path)
                model.load_state_dict(checkpoint["model_state_dict"])
                if optimizer is not None:
                    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
                if return_extra_info:
                    return checkpoint["extra_info"]
            else:
                print(f"{model_name}_v{version}.tar dosen't exist")
    return None


def remove(model_name, version=None, gdrive=False):
    """
    Removes the latest checkpoint.
    If version is provided than it will remove that perticular version.
    """
    path = get_path(model_name, gdrive)
    if path is not None:
        file_names = get_file_names(path)

        if file_names is not None:
            if version is None:
                print(f"Deleting {file_names[-1]}.")
                os.remove(os.path.join(path, file_names[-1]))

            elif os.path.isfile(os.path.join(path, f"{model_name}_v{version}.tar")):
                print(f"Deleting {model_name}_v{version}.tar")
                os.remove(os.path.join(path, f"{model_name}_v{version}.tar"))

            else:
                print(f"{model_name}_v{version}.tar dosen't exist")
