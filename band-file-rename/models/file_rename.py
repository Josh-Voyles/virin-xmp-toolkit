"""
Module Name: file-rename
Author: Josh Voyles
Created: 28 Oct 24

Description:

This is the backed code for my file/metadata rename app.

This module specifically focuses on renaming the files
"""

import os
import shutil
import time

# YYYYMMDD-F-F3965-NNNN


class FileRenamer:
    """A python class desgiend to rename files according to the DoD VIRIN standard YYYYMMDD-F-F3965-NNNN"""

    undo_store = {}

    def __init__(self, path=".") -> None:
        self.path = path
        self.files = os.listdir(path)

    def get_date(self, file) -> str:
        stat = os.stat(f"{self.path}/{file}")  # root path for now
        m_data = time.gmtime(stat.st_mtime)
        c_data = time.gmtime(stat.st_ctime)
        if c_data < m_data:
            return f"{c_data[0]}{c_data[1]:02}{c_data[2]:02}"
        return f"{m_data[0]}{m_data[1]:02}{m_data[2]:02}"

    def get_virin_number(self, date, branch, id, shoot_num, sequence) -> str:
        return f"{date}-{branch}-{id}-{shoot_num}{sequence:03}"

    def rename_all_files(self, ext, shoot_num=0, start_seq=1) -> None:
        self.undo_store.clear()  # clear for 1 level undo (init release)

        previous_date = "YYYYMMDD"
        for file in self.files:
            if os.path.isfile(f"{self.path}/{file}") and f"{self.path}/{file}".endswith(ext):
                date = self.get_date(file)
                if date != previous_date:
                    previous_date = date
                    start_seq = 1
                virin = self.get_virin_number(date, "F", "F3965", shoot_num, start_seq)
                ext = str(file)[-4:]
                self.update_undo_store(file, virin, ext)
                shutil.move(self.path + file, self.path + (virin + ext))
                start_seq += 1

    def update_undo_store(self, file, number, ext) -> None:
        self.undo_store.update({self.path + file: self.path + (number + ext)})

    def undo_rename(self) -> None:
        for key, value in self.undo_store.items():
            shutil.move(value, key)
