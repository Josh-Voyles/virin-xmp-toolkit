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

# Install exiftool
echo "Installing exiftool..."
brew install exiftool

# Install ollama
echo "Installing ollama..."
brew install --cask ollama

# Download and install the Llama 3.18b model
echo "Downloading Llama 3.18b model..."
ollama pull llama3.1

# Function to download and install the latest GitHub release
install_github_release() {
  local repo=$1
  local download_url=https://github.com/${repo}/release/latest/download/virin-xmp-toolkit.zip
  local temp_dir="/tmp/${repo}-${release_tag}"

  # Download the release zip
  echo "Downloading latest release from ${repo}..."
  curl -OL "$download_url"

  # Unzip the downloaded file
  echo "Unzipping release..."
  unzip -q "virin-xmp-toolkit.zip"

  # Move the unzipped files to the Applications folder
  echo "Moving files to /Applications..."
  mv "virin-xmp-toolkit" "~/Desktop"

  # Clean up the temp files
  rm "virin-xmp-toolkit.zip"
}

GITHUB_REPO="josh-voyles/virin-xmp-toolkit"

# Get the latest release tag from GitHub
LATEST_RELEASE_TAG=$(get_latest_release "$GITHUB_REPO")

# Install the latest release from GitHub
install_github_release "$GITHUB_REPO"

# Finished
echo "Installation complete!"
