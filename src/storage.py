import json


class Storage:
    """
    A singleton class responsible for managing and storing parsed data.
    It ensures that only one instance of the class is used throughout the application.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates and returns a singleton instance of the Storage class.
        Returns:
            Storage: The singleton instance of the Storage class.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the Storage object with an empty list to store data.
        """

        self.__data = []

    @property
    def source(self) -> list:
        """
        Gets the list of stored data.
        Returns:
            list: The current list of stored data.
        """

        return self.__data

    @source.setter
    def source(self, data: list) -> None:
        """
        Sets new data by appending it to the current stored data list.
        Args:
            data (list): A list of data to be added to the storage.
        """

        self.__data.extend(data)

    async def save_data(self):
        """
        Asynchronously saves the parsed data to the database.
        This method calls the `update_database` method of the `StorageHandler` class to
        update the database with the current parsed data.
        The parsed data is accessed from the `self.__data` attribute.
        Raises:
            Exception: If there is an issue while saving data to the database.
        """
        from database.core import StorageHandler
        await StorageHandler.update_database(self.__data)