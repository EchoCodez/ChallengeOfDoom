from parse_json import jsonUtils
from data_classes import UserInfo


class MakeDiagnosis:
    def __new__(cls, user_info: UserInfo) -> None:
        self = super().__new__(cls)
        self.user_info = user_info
        return self

if __name__ == "__main__":
    MakeDiagnosis("Bob")
    
