"""
Module Name: file-rename
Author: Josh Voyles
Created: 28 Oct 24

Description:

This module retrieves and batch overwirtes metadata for photo/video files in selected directory.
Will retreive metadata for first file in directory.

Much work needs to be done to support additional meta fields and append to correct location.
"""

import os
from exiftool import ExifToolHelper


class MetaTool:
    """
    Provides functionality to write and retrieve metadata using the ExifTool library.
    The metadata can be added to and extracted from various files based on the file extension.
    """

    def __init__(self) -> None:
        self.meta_fields = {
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
        self._exiftool_path = self._get_exiftool_path()

    def _load_files(self, path, selected_extension) -> list:
        """
        Load files from specified directory.

        Parameters:
            path (str): The directory path containing files to modify.
            selected_extension (str): The file extension filter to select specific files.

        Raises:
            FileNotFoundError: If the specified directory path does not exist.
        """
        try:
            return [
                os.path.join(path, file)
                for file in os.listdir(path)
                if file.lower().endswith(selected_extension)
            ]
        except FileNotFoundError:
            return []

    # handles unix paths
    def _get_exiftool_path(self) -> str:
        """returns first possible path that exists for exiftool installation"""
        possible_paths = [
            "/opt/homebrew/bin/exiftool",
            "/usr/local/bin/exiftool",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return "exiftool"

    def write_metadata(self, path, selected_extension, metadata: dict) -> str:
        """

        Writes metadata to files within the specified directory.

        Parameters:
            path (str): The directory path containing files to modify.
            selected_extension (str): The file extension filter to select specific files.
            metadata (dict): The metadata tags to be written to the selected files.

        Returns:
            str: A message indicating the success or failure of the metadata update operation.

        Raises:
            FileNotFoundError: If the specified directory path does not exist.
        """
        if files := self._load_files(path, selected_extension):
            with ExifToolHelper(executable=self._exiftool_path) as et:
                et.set_tags(files, tags=metadata, params=["-P", "-overwrite_original"])
                et.terminate()
            return "Metadata updated sucessfully!"
        return f"No files found with extension {selected_extension} \
                in {"directory" if path else "(Unspecified directory)"}."

    def retreive_metadata(self, path, selected_extension) -> dict:
        """
        Retrieves metadata from first file of specified directory.

        Args:
            path: The directory path where the files are located.
            selected_extension: The file extension to filter the files.

        Returns:
            A dictionary containing metadata information.
            Default empty values are returned for each key if nothing found.
        """
        # executable="/opt/homebrew/bin/exiftool"
        if files := self._load_files(path, selected_extension):
            with ExifToolHelper(executable=self._exiftool_path) as et:
                tags = et.get_tags(files[0], tags=list(self.meta_fields.keys()))
                for key, value in tags[0].items():
                    key = key.split(":")
                    if len(key) > 1 and key[1] in self.meta_fields:
                        self.meta_fields[key[1]] = value
                et.terminate()
        return self.meta_fields
