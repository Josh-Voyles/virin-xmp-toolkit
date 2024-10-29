from models.file_rename import FileRenamer
import os


def main():
    path = "../../test_folder/"
    fr = FileRenamer(path)

    fr.rename_all_files(".MP4", 0, 1)
    print(*os.listdir(path), sep="\n")
    fr.undo_rename()
    print(*os.listdir(path), sep="\n")


if __name__ == "__main__":
    main()
