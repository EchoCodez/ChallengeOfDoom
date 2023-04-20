import json

class jsonUtils:
    @staticmethod
    def add(*args, file: str = "user-data.json"):
        pass

    @staticmethod
    def clearfile(file: str = "user-data.json"):
        with open(file, "w") as f:
            f.write("{}")
