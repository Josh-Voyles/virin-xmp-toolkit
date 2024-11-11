"""
Module Name: file-rename Author: Josh Voyles
Created: 28 Oct 24

Description:

This module is used to interact will a locally installed Ollama model.
It loads some pre-prompts to make photo/video captioning easier.
"""

from collections.abc import Iterator
import ollama


class VIRINAI:
    """
    VIRINAI class provides methods for initializing and interacting with the Ollama 3.18B model
    """

    def __init__(self) -> None:
        """
        Creates a chat session using the 'llama3.1' model.
        Sends a user's pre-prompt instructions to the model.
        """
        _ = ollama.chat(
            model="llama3.1",
            messages=[
                {
                    "role": "user",
                    "content": self._get_instructions("docs/pre_prompt.txt"),
                }
            ],
            stream=True,
        )

    def _get_instructions(self, path) -> str:
        """
        Reads a file from a specified path and returns its contents as a single string.

        Returns:
            str: The contents of the file.
        """
        with open(path, "r", encoding="utf-8") as file:
            return "\n".join(file.readlines())

    def get_caption(self, details) -> Iterator:
        """
        Generates a caption based on details from a details.txt file and user prompt.

        Returns:
            stream: A stream response from the 'ollama.chat' function
                    using the 'llama3.1' model.
        """
        details = self._get_instructions("docs/details.txt") + "\n" + details

        stream = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": details}],
            stream=True,
        )
        return stream
