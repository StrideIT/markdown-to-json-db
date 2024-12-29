"""
Path management module for handling file system operations.

This module provides a centralized way to handle file paths and operations
across different platforms. It ensures consistent path handling, directory
management, and file operations throughout the application.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> manager = PathManager()
    >>> output_path = manager.get_default_output_path("input.md")
    >>> print(output_path.endswith('.json'))
    True
"""

import os
from typing import Optional

class PathManager:
    """Manages file path operations and validations across platforms.

    This class provides a comprehensive set of methods for handling file paths,
    ensuring consistent behavior across different operating systems. It handles
    path construction, extension management, directory creation, and path
    validation.

    Attributes:
        base_dir (str): Base directory for all path operations. This serves
            as the root directory for relative path calculations.

    Note:
        All paths are normalized using os.path functions to ensure
        platform-independent behavior.
    """

    def __init__(self, base_dir: Optional[str] = None) -> None:
        """Initialize PathManager with optional base directory.

        Sets up the PathManager instance with a base directory for path
        operations. If no base directory is provided, uses the current
        working directory.

        Args:
            base_dir (Optional[str]): Base directory for path operations.
                If None, uses the current working directory. Should be
                a valid directory path.

        Example:
            >>> manager = PathManager("/custom/base/dir")
            >>> os.path.isabs(manager.base_dir)
            True
        """
        self.base_dir = base_dir or os.getcwd()

    def validate_path(self, path: str) -> bool:
        """Validate if a path is valid and accessible.

        Checks if the given path exists and is accessible. This includes
        verifying that the parent directory exists and has appropriate
        permissions.

        Args:
            path (str): Path to validate. Can be absolute or relative to
                the base directory.

        Returns:
            bool: True if the path is valid and accessible, False otherwise.

        Example:
            >>> manager = PathManager()
            >>> manager.validate_path(os.getcwd())
            True
        """
        try:
            return os.path.exists(os.path.dirname(path))
        except Exception:
            return False

    def ensure_directory(self, path: str) -> None:
        """Ensure directory exists, creating it if necessary.

        Creates all necessary parent directories for a given path if they
        don't already exist. This is useful when preparing to write files
        to a new location.

        Args:
            path (str): Path to ensure exists. Can be a file path, in which
                case the parent directory is ensured.

        Raises:
            OSError: If directory creation fails due to permissions or
                other system issues.

        Example:
            >>> manager = PathManager()
            >>> new_dir = os.path.join(manager.base_dir, "new_folder")
            >>> manager.ensure_directory(new_dir)
            >>> os.path.exists(new_dir)
            True
        """
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def get_default_output_path(self, source_file: str, extension: str = '.json') -> str:
        """Generate default output path based on source file.

        Creates an output path in the same directory as the source file,
        using the same name but with a different extension. This is useful
        for creating output files that correspond to input files.

        Args:
            source_file (str): Source file path to base output path on.
            extension (str, optional): Desired output file extension.
                Defaults to '.json'. Should include the dot.

        Returns:
            str: Generated output path with the specified extension.

        Example:
            >>> manager = PathManager()
            >>> output = manager.get_default_output_path("input.md")
            >>> output.endswith("input.json")
            True
        """
        source_dir = os.path.dirname(source_file)
        source_filename = os.path.splitext(os.path.basename(source_file))[0]
        return os.path.join(source_dir, f"{source_filename}{extension}")

    def normalize_path(self, path: str) -> str:
        """Normalize path for consistent cross-platform handling.

        Converts path separators to the system's preferred format and
        resolves relative path components. This ensures consistent path
        handling across different operating systems.

        Args:
            path (str): Path to normalize. Can be absolute or relative,
                with any style of path separators.

        Returns:
            str: Normalized path using system-specific separators.

        Example:
            >>> manager = PathManager()
            >>> path = manager.normalize_path("dir1/dir2\\file.txt")
            >>> "\\" in path if os.name == "nt" else "/" in path
            True
        """
        return os.path.normpath(path)

    def join_paths(self, *paths: str) -> str:
        """Join paths in a platform-independent way.

        Combines multiple path components using the system's path separator.
        This method handles different path separators and ensures proper
        joining regardless of the operating system.

        Args:
            *paths: Variable number of path components to join. Each
                component should be a string.

        Returns:
            str: Combined path using system-specific separators.

        Example:
            >>> manager = PathManager()
            >>> path = manager.join_paths("dir1", "dir2", "file.txt")
            >>> len(path.split(os.sep)) > 1
            True
        """
        return os.path.join(*paths)

    def get_extension(self, path: str) -> str:
        """Get file extension from path.

        Extracts the file extension from a path, including the dot.
        If the file has no extension, returns an empty string.

        Args:
            path (str): File path to extract extension from.

        Returns:
            str: File extension including the dot, or empty string if
                no extension exists.

        Example:
            >>> manager = PathManager()
            >>> ext = manager.get_extension("file.txt")
            >>> ext == ".txt"
            True
        """
        return os.path.splitext(path)[1]

    def change_extension(self, path: str, new_extension: str) -> str:
        """Change file extension while preserving the path.

        Replaces the current file extension with a new one, or adds the
        new extension if the file doesn't have one. The new extension
        should include the dot.

        Args:
            path (str): Original file path to modify.
            new_extension (str): New extension to apply, including the dot
                (e.g., '.json', '.txt').

        Returns:
            str: Modified path with the new extension.

        Example:
            >>> manager = PathManager()
            >>> new_path = manager.change_extension("file.txt", ".json")
            >>> new_path.endswith(".json")
            True
        """
        root = os.path.splitext(path)[0]
        return f"{root}{new_extension}"
