"""syphon.core.archive.lockmanager.py

   Copyright Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/tektronix/syphon/blob/master/LICENSE)

"""
import os
from typing import List


class LockManager(object):
    """Lock file helper.

    A lock file is any file named #lock. Lock files allow
    communication between programs with lock file support to prevent
    the removal of files that may be in use.
    """

    def __init__(self):
        super().__init__()
        self._filename = "#lock"
        self._locks: List[str] = list()

    @property
    def filename(self) -> str:
        """Lock file name."""
        return self._filename

    @property
    def locks(self) -> list:
        """List of current lock files."""
        return self._locks

    @staticmethod
    def _delete(filepath: str):
        """Delete a given file.

        Raises:
            OSError: File operation error. Error type raised may be
                a subclass of OSError.
        """
        os.remove(filepath)

    @staticmethod
    def _touch(filepath: str):
        """Linux touch-like command.

        Raises:
            OSError: File operation error. Error type raised may be
                a subclass of OSError.
        """
        with open(filepath, "a"):
            os.utime(filepath, None)

    def lock(self, path: str) -> str:
        """Create a lock file in a given directory.

        Args:
            path (str): Directory to lock.

        Returns:
            str: Absolute filepath of the created lock file.

        Raises:
            OSError: File operation error. Error type raised may be
                a subclass of OSError.
        """
        filepath = os.path.join(os.path.abspath(path), self.filename)

        LockManager._touch(filepath)

        if filepath not in self._locks:
            self._locks.append(filepath)

        return filepath

    def release(self, filepath: str):
        """Remove the given lock file.

        Args:
            filepath (str): Location of a lock file.

        Raises:
            OSError: File operation error. Error type raised may be
                a subclass of OSError.
        """
        fullpath: str = os.path.abspath(filepath)

        if fullpath in self._locks:
            self._locks.remove(fullpath)
            try:
                LockManager._delete(fullpath)
            except FileNotFoundError:
                pass

    def release_all(self):
        """Remove all lock files.

        Raises:
            OSError: File operation error. Error type raised may be
                a subclass of OSError.
        """
        while len(self._locks) != 0:
            lock = self._locks.pop()
            try:
                LockManager._delete(lock)
            except FileNotFoundError:
                pass
