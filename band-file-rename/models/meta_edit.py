import os
import subprocess
import shlex


class MetaTool:

    def write_meta_data(self, path, selected_extension, metadata_options="") -> None:
        """Triggers exiftool to write metadata"""
        arguements = [
            "exiftool",
            "-overwrite_original",
            f"-ext {selected_extension}",
            metadata_options,
            path,  # need to handle paths on windows differently
        ]
        command = " ".join(arguements)
        os.system(command)

    def retreive_metadata(self, path, selected_extension) -> dict:
        var = ""
        path = os.path.abspath(path)
        dir = os.listdir(path)
        for file in dir:
            _, ext = os.path.splitext(file)
            if ext[1:].lower() == selected_extension:
                var = subprocess.check_output(
                    f"exiftool {shlex.quote(os.path.join(path, file))}"
                )
                break
        print(var)

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
