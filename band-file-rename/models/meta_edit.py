import exiftool
import os


class MetaTool:
    def __init__(self, path=".") -> None:
        self.path = path
        self.files = os.listdir(path)

    def get_meta_data(self):
        et = exiftool.ExifToolHelper()
        metadata = et.get_metadata(self.files)
        for d in metadata:
            print(d)


def main():
    print("just under main")
    tool = MetaTool()
    print("tool created")
    tool.get_meta_data()


if __name__ == "__main__":
    main()
