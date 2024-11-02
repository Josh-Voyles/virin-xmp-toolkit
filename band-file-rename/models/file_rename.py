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

# YYYYMMDD-F-F3965-NNNN


class FileRenamer:
    """A python class desgiend to rename files according to the DoD VIRIN standard YYYYMMDD-F-F3965-NNNN"""

    # list of dictionaries (undo is unlimited as long as program is open)
    undo_store = []

    def get_date(self, path, file) -> str:
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
    ) -> None:
        undo_dict = {}
        path = os.path.abspath(path)

        sequence_number = start_seq

        fixed_date = ""
        if date:
            fixed_date = date

        previous_date = "YYYYMMDD"
        for file in self.get_files_sorted(path):
            _, ext = os.path.splitext(file)
            if ext[1:].lower() == selected_extension:
                if not fixed_date:
                    date = self.get_date(path, file)
                if date != previous_date:
                    previous_date = date
                    sequence_number = start_seq
                new_filename = self.get_virin_number(
                    date, "F", "F3965", shoot_num, sequence_number
                )
                try:
                    if file == new_filename + ext:
                        raise FileExistsError
                    os.rename(
                        os.path.join(path, file), os.path.join(path, new_filename + ext)
                    )
                    undo_dict.update(
                        {
                            os.path.join(path, file): os.path.join(
                                path, new_filename + ext
                            )
                        }
                    )
                    sequence_number += 1
                except FileNotFoundError as f:
                    print("File not found: ", f)
                except PermissionError as p:
                    print(
                        "You do not have the correct permissions to modify this file: ",
                        p,
                    )
                except IsADirectoryError:
                    print("You are trying to modify as directory!")
                except FileExistsError as f:
                    print("File exsists already!: ", f)

                except OSError as e:
                    print("An error has occured with the OS module: ", e)
        if undo_dict != {}:
            self.undo_store.append(undo_dict)

    def undo_rename(self) -> None:
        if self.undo_store:
            d = self.undo_store.pop()
            for key, value in d.items():
                os.rename(value, key)
