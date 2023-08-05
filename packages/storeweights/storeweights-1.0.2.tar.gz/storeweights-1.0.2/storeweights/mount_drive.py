import os


def gdrive(model_name):
    """
    Mounting google drive (Only supports Google colab)
    """
    if not os.path.isdir("gdrive"):
        try:
            from google.colab import drive

            drive.mount(os.path.join(os.getcwd(), "gdrive"))
        except ModuleNotFoundError:
            print("Currently Google Drive is supported only in Colab")
            return None

    path = os.path.join("gdrive", "My Drive", model_name)
    return path
