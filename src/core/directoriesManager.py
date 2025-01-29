from src.utils.settings import DATA_DIR

import os

class DirectoriesManager():

    @staticmethod
    def create_directory(self, directory) -> None:
        """
        Creates a directory if it does not exist.

        :param directory: The directory to create.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def create_directory_in_data(self, directory) -> None:
        """
        Creates a directory in the data directory if it does not exist.

        :param directory: The directory to create.
        """
        self.create_directory(os.path.join(DATA_DIR, directory))

    @staticmethod
    def is_directory_exists(self, directory) -> bool:
        """
        Checks if a directory exists.

        :param directory: The directory to check.
        :return: True if the directory exists, False otherwise.
        """
        return os.path.exists(directory)
    
    @staticmethod
    def is_directory_exists_in_data(self, directory) -> bool:
        """
        Checks if a directory exists in the data directory.

        :param directory: The directory to check.
        :return: True if the directory exists, False otherwise.
        """
        return self.is_directory_exists(DATA_DIR)