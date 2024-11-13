# virin-xmp-toolkit

---

## Install

macOS Only (For time being)

virin-xmp-toolkit requires Phil Harvey's exiftool and Ollama.

However, the installer will install these dependencies and Homebrew if not already installed.

```bash
curl -sSL https://raw.githubusercontent.com/josh-voyles/virin-xmp-toolkit/main/install.sh | bash
```

## Uninstall

```bash
brew uninstall exiftool
brew uninstall ollama

# warning (code below may uninstall other packages you installed with brew)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
sudo rm -rf /opt/homebrew
```

# Instructions

---

## File Renaming

virin-xmp-toolkit uses the DOD virin (visual information record identification number) standard to help the Air Force Band production team rename files.

The teams visual ID is currently hard-coded into the program since this tool is meant for internal usage.

A common mistake will be to not select the correct file format.

### Functions

- (Folder) - Select the parent directory of the files you want to batch process.
- (File Format) - List of file formats currently supported by the renaming function.
- (Reset) - Resets all fields.
- (Undo) - Unlimited undos as long as application is open. (WARNING: Do not change folder contents while using the app).
- (Rename) - Rename all files in the folder with the selected file format.
- (Date Override) - Tool will normally extract date from metadata. However, you can input your own date.
- (Shot#) - Select the shoot or camera
- (Seq#) - Starting sequence number. Normally you will choose 1.

## Metadata

### Functions

- (Folder) - Select the parent directory of the files you want to batch process.
- (File Format) - List of file formats currently supported by the metadata function.
- (Creator) - Defaults to USAF Band Production when clear button is used
- (Title) - Your thrilling headline for the series of photos for videos
- (Description) - The photo/video caption using AP guidelines AF style.
- (Writer) - Who wrote the caption (from my understanding)
- (Keywords) - Defaults to USAFBand when clear button is clicked
- (City, State, Country) - self-explanatory
- (Copyright) - Will also default to Public Domain. (non-editable)
- (Load) - Loads metadata from first file in directory that matches file format.
- (Clear) - Clear all fields and creates defaults for Creator, Keywords, and Copyright.
- (Write) - Writes metadata to all files with chosen format based on input fields.

## AI caption

- (Left Box) - Write a description of your video shoot or photo shoot. Provide many details.
- (Right Box) - Ollama will spit out a basic caption to help you with writing yours.
- (Reset) - Resets all text boxes to empty.
- (Submit) - Sends your prompt to Ollama

## Quit

- Quits application.
