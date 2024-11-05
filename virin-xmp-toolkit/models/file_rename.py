"""
Module Name: file-rename
Author: Josh Voyles
Created: 28 Oct 24

Description:

This is the backed code for my file/metadata rename app.

This module specifically focuses on renaming the files
"""

import os
import time
import traceback

# YYYYMMDD-F-F3965-NNNN


class FileRenamer:
    """A python class desgiend to rename files according to the DoD VIRIN standard YYYYMMDD-F-F3965-NNNN"""

    # list of dictionaries (undo is unlimited as long as program is open)
    undo_store = []
    directory_size = []

    def get_formatted_date(self, path, file) -> str:
        stat = os.stat(os.path.join(path, file))  # root path for now
        m_data = time.gmtime(stat.st_mtime)
        c_data = time.gmtime(stat.st_ctime)
        if c_data < m_data:
            return f"{c_data[0]}{c_data[1]:02}{c_data[2]:02}"
        return f"{m_data[0]}{m_data[1]:02}{m_data[2]:02}"

    def get_virin_number(self, date, branch, id, shoot_num, sequence) -> str:
        return f"{date}-{branch}-{id}-{shoot_num}{sequence:03}"

    def get_files_sorted(self, path):
        def get_time(file):
            file_path = os.path.join(path, file)
            c_time = os.path.getctime(file_path)
            m_time = os.path.getmtime(file_path)
            if m_time < c_time:
                return m_time
            return c_time

        return sorted(os.listdir(path), key=get_time)

    def rename_all_files(
        self, path, selected_extension, date, shoot_num=0, start_seq=1
    ) -> str:
        undo_dict = {}
        notification = ""
        path = os.path.abspath(path)
        sequence_number = start_seq

        fixed_date = ""
        if date:
            fixed_date = date

        previous_date = "YYYYMMDD"
        sorted_files = self.get_files_sorted(path)

        for file in sorted_files:
            old_filename, ext = os.path.splitext(file)
            if ext[1:].lower() == selected_extension:
                if not fixed_date:
                    date = self.get_formatted_date(path, file)
                if date != previous_date:
                    previous_date = date
                    sequence_number = start_seq

                new_filename = self.get_virin_number(
                    date, "F", "F3965", shoot_num, sequence_number
                )
                sequence_number += 1  # must increment here to prevent overwrite files on repeat accidental rename

                try:
                    if new_filename == old_filename:
                        raise FileExistsError
                    os.rename(
                        os.path.join(path, file), os.path.join(path, new_filename + ext)
                    )
                    notification += f"{old_filename} > {new_filename}\n"
                    undo_dict.update(
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
                    notification += f"An error has occured with the OS module! Please copy error and send to Josh!\n{traceback.format_exc()}"

        if undo_dict != {}:
            self.undo_store.append(undo_dict)
            self.directory_size.append(len(sorted_files))

        return (
            f"Could not find any files with extension {selected_extension}"
            if not notification
            else notification
        )

    def directory_is_modified(self, undo_dict) -> str:
        notification = ""
        path, _ = os.path.split(list(undo_dict.keys())[0])
        current_dir_size = len(os.listdir(path))
        actual_dir_size = self.directory_size.pop()
        if actual_dir_size != current_dir_size:
            notification += (
                "Target directory has been modified. Unable to undo! Expected:\n"
            )
            for _, value in undo_dict.items():
                notification += value + "\n"
            self.directory_size.append(actual_dir_size)
            return notification
        return notification

    def process_undo(self, undo_dict):
        notification = "Undo proceedure stats:\n\n"
        # We put back newer name (value) to original (key)
        for key, value in reversed(undo_dict.items()):
            dir, old_file = os.path.split(key)
            _, new_file = os.path.split(value)
            try:
                if old_file in os.listdir(dir):
                    raise FileExistsError
                os.rename(value, key)
                notification += f"{new_file} > {old_file}\n"
            except FileNotFoundError:
                notification += f"File not found to undo! {key}\n"
            except FileExistsError:
                notification += f"This file exists and undo failed! {old_file}\n"
        return notification

    def undo_rename(self) -> str:
        if self.undo_store:
            undo_dict = self.undo_store.pop()
            notification = self.directory_is_modified(undo_dict)
            if not notification:
                return self.process_undo(undo_dict)
            self.undo_store.append(undo_dict)
            return notification
        return "Nothing to undo"
