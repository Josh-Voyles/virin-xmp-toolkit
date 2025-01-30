#!/bin/bash

# Exit script on any error
set -e

# Function to check if a command is available
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Install Homebrew if it isn't installed
if ! command_exists brew; then
  echo "Homebrew not found. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Found Homebrew. Using Homebrew."
fi

# Check if brew is in the PATH
if ! command -v brew &>/dev/null; then
  # If not found, add Homebrew to PATH
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >>~/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Install exiftool
echo "Installing exiftool..."
brew install exiftool

# Install ollama
echo "Installing ollama..."
brew install --cask ollama

# Download and install the Llama 3.18b model
echo "Downloading Llama 3.18b model..."
ollama pull llama3.2

# Function to download and install the latest GitHub release
install_github_release() {
  local repo=$1
  local download_url=https://github.com/${repo}/releases/latest/download/virin-xmp-toolkit.zip
  local old_folder=/Users/$USER/Desktop/virin-xmp-toolkit.app
  local new_location=/Users/$USER/Desktop/
  if [ -d ${old_folder} ]; then
    echo "Deleting old target folder..."
    rm -rf ${old_folder}
  fi

  # Download the release zip
  echo "Downloading latest release from ${repo}..."
  curl -OL "$download_url"

  # Unzip the downloaded file
  echo "Unzipping release..."
  unzip -o "virin-xmp-toolkit.zip" -d ${new_location}

  # Clean up the zip file
  rm "virin-xmp-toolkit.zip"
}

GITHUB_REPO="josh-voyles/virin-xmp-toolkit"

# Install the latest release from GitHub
install_github_release "$GITHUB_REPO"

# Finished
echo "Installation complete!"
