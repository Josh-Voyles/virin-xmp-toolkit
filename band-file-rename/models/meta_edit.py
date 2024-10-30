import os

PATH_TO_TEST_FILES = "/home/joshvoyles/Documents/band-file-rename/band-file-rename/tests/test_data/"

class MetaTool:
            
    def write_meta_data(self, ext="", metadata_options="", path = ".") -> None:
        """Triggers exiftool to write metadata"""
        arguements = [
            "exiftool",
            "-overwrite_original",
            f"-ext {ext}",
            metadata_options,
            path,  # need to handle paths on windows differently
        ]
        command = " ".join(arguements)
        os.system(command)


    # This function may be used in future if we need to append date
    # def get_date(self, file):
    #     stat = os.stat(f"{self.path}/{file}")  # root path for now
    #     m_data = time.gmtime(stat.st_mtime)
    #     c_data = time.gmtime(stat.st_ctime)
    #     if c_data < m_data:
    #         print("C Time: ",time.strftime("%Y-%m-%dT%H:%M:%S", c_data))
    #         return time.strftime("%Y-%m-%d %H:%M:%S", m_data)
    #     print("M Time: ",time.strftime("%Y-%m-%dT%H:%M:%S", m_data))
    #     return time.strftime("%Y-%m-%d %H:%M:%S", m_data)


def main():
    tool = MetaTool()
    tool.write_meta_data('mp4', path=PATH_TO_TEST_FILES)
    
    # Possible metadata options
    # f"-creator={repr(creator)}",
    # f"-title={repr(title)}",
    # f"-headline={repr(title)}",
    # f"-description={repr(description)}",
    # f"-writer={repr(writer)}",
    # f"-keywords={repr(keywords)}",
    # f"-city={repr(city)}",
    # f"-state={repr(state)}",
    # f"-country={repr(country)}",
    # "-copyright='Public Domain'",
    # "-rights='Public Domain'",


if __name__ == "__main__":
    main()
