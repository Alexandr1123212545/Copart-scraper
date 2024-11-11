
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

    def save_data(self):
        from database.core import StorageHandler
        # json_data = json.dumps(self.__data, ensure_ascii=False, indent=4)
        # with open('../saved_data_test.json', 'w', encoding='utf-8') as file:
        #     file.write(json_data)
        StorageHandler.update_data(self.__data)