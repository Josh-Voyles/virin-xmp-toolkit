import os
import exiftool
from exiftool import ExifToolHelper


class MetaTool:

    def write_metadata(self, path, selected_extension, metadata: dict) -> str:
        """Triggers exiftool to write metadata"""
        files = []
        try:
            files = [
                os.path.join(path, file)
                for file in os.listdir(path)
                if file.lower().endswith(selected_extension)
            ]
        except FileNotFoundError:
            return "Please choose a folder."
        if files:
            with ExifToolHelper() as et:
                et.set_tags(files, tags=metadata, params=["-P", "-overwrite_original"])
                et.terminate()
            return "Metadata updated sucessfully!"
        return f"No files found with extension {selected_extension}."

    def retreive_metadata(self, path, selected_extension) -> dict:
        data = {
            "Creator": "",
            "Writer": "",
            "Description": "",
            "Title": "",
            "Keywords": "",
            "City": "",
            "Country": "",
            "Headline": "",
            "State": "",
            "Copyright": "",
        }
        try:
            files = [
                os.path.join(path, file)
                for file in os.listdir(path)
                if file.lower().endswith(selected_extension)
            ]
        except FileNotFoundError:
            return data

        # in the function, we will just display meta of first file since batch processing
        if files:
            with ExifToolHelper() as et:
                tags = et.get_tags(
                    files[0],
                    tags=[
                        "Creator",
                        "Writer",
                        "Description",
                        "Title",
                        "Keywords",
                        "City",
                        "Country",
                        "Headline",
                        "State",
                        "Copyright",
                    ],
                )
                for key, value in tags[0].items():
                    key = key.split(":")
                    if len(key) > 1 and key[1] in data:
                        data[key[1]] = value if data[key[1]] == "" else data[key[1]]
                et.terminate()
        return data
