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
brew install ollama

# Download and install the Llama 3.18b model
echo "Downloading Llama 3.18b model..."
ollama pull llama3.1

# Function to get the latest GitHub release
get_latest_release() {
  local repo=$1
  # Use GitHub's API to fetch the latest release
  curl --silent "https://api.github.com/repos/$repo/releases/latest" | jq -r .tag_name
}

# Function to download and install the latest GitHub release
install_github_release() {
  local repo=$1
  local release_tag=$2
  local download_url="https://github.com/${repo}/releases/download/${release_tag}/${repo}-${release_tag}.zip"
  local temp_dir="/tmp/${repo}-${release_tag}"

  # Download the release zip
  echo "Downloading release ${release_tag} from ${repo}..."
  curl -L -o "${temp_dir}.zip" "$download_url"

  # Unzip the downloaded file
  echo "Unzipping release..."
  unzip -q "${temp_dir}.zip" -d "${temp_dir}"

  # Move the unzipped files to the Applications folder
  echo "Moving files to /Applications..."
  mv "${temp_dir}" "/Applications/${repo}"

  # Clean up the temp files
  rm -rf "${temp_dir}.zip" "${temp_dir}"
}

GITHUB_REPO="josh-voyles/virin-xmp-toolkit"

# Get the latest release tag from GitHub
LATEST_RELEASE_TAG=$(get_latest_release "$GITHUB_REPO")

# Install the latest release from GitHub
install_github_release "$GITHUB_REPO" "$LATEST_RELEASE_TAG"

# Finished
echo "Installation complete!"
