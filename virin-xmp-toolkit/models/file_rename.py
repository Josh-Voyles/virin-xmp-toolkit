"""
Module Name: file-rename
Author: Josh Voyles
Created: 28 Oct 24

Description:

This module batch-renames files in selected directory using the os module.

"""

import os
import time
import traceback


EMPTY_STRING = ""
SERVICE_BRANCH = "F"
VIRIN_ID = "F3965"


class FileRenamer:
    """
    Renames files according to the DoD VIRIN (Visual Information Record Identification Number) standard YYYYMMDD-F-F3965-NNNN
    """

    write_actions = (
        []
    )  # list of write actions  (undo is unlimited as long as program is open)
    directory_size = (
        []
    )  # for measuring size of directory. Used to validate directory size

    def _get_formatted_date(self, path, file) -> str:
        """
        Retrieves the modified or created date from file.
        Sometimes (on Unix) it seems modified date is used by default.
        Will use lowest and return date in YYYYMMDD format.

        Returns:
            str: A string representing the formatted date in 'YYYYMMDD' format.
        """
        stat = os.stat(os.path.join(path, file))
        m_data = time.gmtime(stat.st_mtime)
        c_data = time.gmtime(stat.st_ctime)
        if c_data < m_data:
            return f"{c_data[0]}{c_data[1]:02}{c_data[2]:02}"
        return f"{m_data[0]}{m_data[1]:02}{m_data[2]:02}"

    def _get_virin_number(self, date, branch, virin, shoot_num, sequence) -> str:
        """
        Generate a VIRIN  based on the provided parameters.

        Returns:
        str: A formatted VIRIN string.
        """
        return f"{date}-{branch}-{virin}-{shoot_num}{sequence:03}"

    def _get_files_sorted(self, path):
        """
        Returns a list of files in the specified directory, sorted by their creation or modification time.
        If the modification time of a file is earlier than its creation time, the modification time is used for sorting.

        Args:
            path (str): The path to the directory to list files from.

        Returns:
            list: A list of filenames sorted by their creation or modification time.
        """

        def _get_time(file):
            file_path = os.path.join(path, file)
            c_time = os.path.getctime(file_path)
            m_time = os.path.getmtime(file_path)
            if m_time < c_time:
                return m_time
            return c_time

        return sorted(os.listdir(path), key=_get_time)

    def _is_directory_modified(self, single_write_action) -> str:
        """
        Checks if the target directory has been modified after an operation that affects file integrity.

        Args:
            single_write_action : dict of file changes for one write action

        Returns:
            str: A notification message if the directory has been modified; otherwise, an empty string.
        """
        notification = EMPTY_STRING
        path, _ = os.path.split(list(single_write_action.keys())[0])
        current_dir_size = len(os.listdir(path))
        actual_dir_size = self.directory_size.pop()
        if actual_dir_size != current_dir_size:
            notification += (
                "Target directory has been modified. Unable to undo! Expected:\n"
            )
            for _, value in single_write_action.items():
                notification += value + "\n"
            self.directory_size.append(actual_dir_size)
            return notification
        return notification

    def rename_all_files(
        self, path, selected_extension, date, shoot_num, start_seq
    ) -> str:
        """
        Renames all files with a specified extension in the provided directory according to a VIRIN

        Parameters:
            path (str): The directory path containing the files to rename.
            selected_extension (str): The file extension of the files to be renamed.
            date (str): Option fixed date to override _get_formatted_date
            shoot_num (int): The shoot number to include in the new name of the files.
            start_seq (int): The starting sequence number for the renaming process.

        Returns:
            str: A notification message detailing the outcome of the renaming process.

        Exceptions:
            Handles various exceptions and appends errors to return string.
        """
        # init starting variables
        notification, fixed_date, previous_date = EMPTY_STRING
        single_write_action = {}
        path = os.path.abspath(path)
        sequence_number = start_seq

        if date:
            fixed_date = date

        sorted_files = self._get_files_sorted(path)

        for file in sorted_files:
            old_filename, ext = os.path.splitext(file)
            if ext[1:].lower() == selected_extension:

                if not fixed_date:
                    date = self._get_formatted_date(path, file)
                # When encountering new date, we must start new sequence
                if date != previous_date:
                    previous_date = date
                    sequence_number = start_seq

                new_filename = self._get_virin_number(
                    date, SERVICE_BRANCH, VIRIN_ID, shoot_num, sequence_number
                )
                # must increment here to prevent overwrite files on repeat accidental rename
                sequence_number += 1

                try:
                    if new_filename == old_filename:
                        raise FileExistsError
                    os.rename(
                        os.path.join(path, file), os.path.join(path, new_filename + ext)
                    )
                    notification += f"{old_filename} > {new_filename}\n"
                    single_write_action.update(
                        {
                            os.path.join(path, file): os.path.join(
                                path, new_filename + ext
                            )
                        }
                    )
                except FileNotFoundError:
                    notification += f"File not found: {old_filename}\n"
                except PermissionError:
                    notification += f"Permission Denied: {old_filename}\n"
                except IsADirectoryError:
                    notification += f"Error: Is a directory: {old_filename}\n"
                except FileExistsError:
                    notification += f"File already exists: {old_filename}\n"
                except OSError:
                    notification += f"An error has occured with the OS module! \
                        Please copy error and submit issue!\n{traceback.format_exc()}"

        if single_write_action:
            self.write_actions.append(single_write_action)
            self.directory_size.append(len(sorted_files))

        return (
            f"Could not find any files with extension {selected_extension}"
            if not notification
            else notification
        )

    def _revert_to_original(self, single_write_action):
        """
        Processes the undo operation for a dictionary of file operations.

        Returns:
        str: A notification message summarizing the results of the undo operation.

        Raises:
        FileNotFoundError: If the file that is supposed to be renamed back is not found.
        FileExistsError: If a file with the original name already exists in the directory.
        """
        notification = "Undo proceedure stats:\n\n"
        # We put back newer name (value) to original (key)
        for key, value in reversed(single_write_action.items()):
            directory, old_file = os.path.split(key)
            _, new_file = os.path.split(value)
            try:
                if old_file in os.listdir(directory):
                    raise FileExistsError
                os.rename(value, key)
                notification += f"{new_file} > {old_file}\n"
            except FileNotFoundError:
                notification += f"File not found to undo! {key}\n"
            except FileExistsError:
                notification += f"This file exists and undo failed! {old_file}\n"
        return notification

    def undo_rename(self) -> str:
        """
        Reverts the last renaming action performed and restores the previous state.

        Returns:
            str: Indicates the result of the undo operation.
        """
        if self.write_actions:
            single_write_action = self.write_actions.pop()
            notification = self._is_directory_modified(single_write_action)
            if not notification:
                return self._revert_to_original(single_write_action)
            # put back to giver user chance to fix w/o loosing undo
            self.write_actions.append(single_write_action)
            return notification
        return "Nothing to undo"
