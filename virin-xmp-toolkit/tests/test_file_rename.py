import pytest
import shutil
import os
from models.file_rename import FileRenamer

SOURCE_TEST_FILES = "./tests/test_data/"
DESTINATION_TEST_FILES = "./tests/temp_test_data/"
PATH_TO_TEST_FILES_RENAMER = os.path.join(os.path.dirname(__file__), "temp_test_data/")
shutil.copytree(SOURCE_TEST_FILES, DESTINATION_TEST_FILES)


@pytest.fixture
def renamer():
    return FileRenamer(PATH_TO_TEST_FILES_RENAMER)


def test_rename_all_files(renamer):

    old_tree = [
        "MVI_0902.MP4",
        "MVI_0903.MP4",
        "MVI_0904.MP4",
        "MVI_0905.MP4",
        "MVI_0906.MP4",
        "MVI_0907.MP4",
        "MVI_0908.MP4",
        "MVI_0909.MP4",
        "MVI_0910.MP4",
        "MVI_0911.MP4",
        "MVI_0912.MP4",
        "MVI_0913.MP4",
        "MVI_0914.MP4",
        "MVI_0915.MP4",
        "MVI_0916.MP4",
        "MVI_0917.MP4",
        "MVI_0918.MP4",
        "MVI_0919.MP4",
        "MVI_0920.MP4",
        "MVI_0921.MP4",
        "MVI_0922.MP4",
        "MVI_0923.MP4",
        "MVI_0924.MP4",
        "MVI_0925.MP4",
        "MVI_0926.MP4",
        "Terry Concert",
    ]

    new_tree = [
        "Terry Concert",
        "20220712-F-F3965-0001.MP4",
        "20220712-F-F3965-0002.MP4",
        "20220712-F-F3965-0003.MP4",
        "20220712-F-F3965-0004.MP4",
        "20220712-F-F3965-0005.MP4",
        "20220713-F-F3965-0001.MP4",
        "20220713-F-F3965-0002.MP4",
        "20220713-F-F3965-0003.MP4",
        "20220713-F-F3965-0004.MP4",
        "20220713-F-F3965-0005.MP4",
        "20220713-F-F3965-0006.MP4",
        "20220713-F-F3965-0007.MP4",
        "20220713-F-F3965-0008.MP4",
        "20220713-F-F3965-0009.MP4",
        "20220713-F-F3965-0010.MP4",
        "20220713-F-F3965-0011.MP4",
        "20220713-F-F3965-0012.MP4",
        "20220713-F-F3965-0013.MP4",
        "20220713-F-F3965-0014.MP4",
        "20220713-F-F3965-0015.MP4",
        "20220713-F-F3965-0016.MP4",
        "20220713-F-F3965-0017.MP4",
        "20220713-F-F3965-0018.MP4",
        "20220713-F-F3965-0019.MP4",
        "20220713-F-F3965-0020.MP4",
    ]

    assert os.listdir(DESTINATION_TEST_FILES) == old_tree

    renamer.rename_all_files(".MP4", 0, 1)

    assert os.listdir(DESTINATION_TEST_FILES) == new_tree


def test_undo(renamer):
    old_tree = [
        "Terry Concert",
        "MVI_0902.MP4",
        "MVI_0903.MP4",
        "MVI_0904.MP4",
        "MVI_0905.MP4",
        "MVI_0906.MP4",
        "MVI_0907.MP4",
        "MVI_0908.MP4",
        "MVI_0909.MP4",
        "MVI_0910.MP4",
        "MVI_0911.MP4",
        "MVI_0912.MP4",
        "MVI_0913.MP4",
        "MVI_0914.MP4",
        "MVI_0915.MP4",
        "MVI_0916.MP4",
        "MVI_0917.MP4",
        "MVI_0918.MP4",
        "MVI_0919.MP4",
        "MVI_0920.MP4",
        "MVI_0921.MP4",
        "MVI_0922.MP4",
        "MVI_0923.MP4",
        "MVI_0924.MP4",
        "MVI_0925.MP4",
        "MVI_0926.MP4",
    ]
    renamer.undo_rename()
    assert os.listdir(DESTINATION_TEST_FILES) == old_tree


def test_end():
    shutil.rmtree(DESTINATION_TEST_FILES)
