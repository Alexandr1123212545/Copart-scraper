import json


class Storage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__data = []

    @property
    def source(self) -> list:
        return self.__data

    @source.setter
    def source(self, data: list) -> None:
        self.__data.extend(data)

    async def save_data(self):

        try:
            with open("data.json", "w", encoding="utf-8") as file:
                json.dump(self.__data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Wrong write json: {e}")

        from database.core import StorageHandler
        await StorageHandler.update_database(self.__data)