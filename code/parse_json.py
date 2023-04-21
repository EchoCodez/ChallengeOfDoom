import json
from typing import Callable
from io import StringIO
from dataclasses import dataclass



preferences = ("appearance_theme", "save_data")
files = ("preferences.json", "user-data.json")


@dataclass
class UserInfo:
    conditions: list[str]
    preferences: dict[str, bool]
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}:\n\tconditions={self.conditions}\n\tpreferences={self.preferences}"


class jsonUtils:
    '''Class containing custom made json file uses'''
    @staticmethod
    def add(data: dict, file: str = "user-data.json", indent=4):
        '''
        Adds data to a file
        
        Parameters
        ----------
        data: dict
            The data to be added. If it is not added, raises TypeError
        file: str = "user-data.json"
            Which file to add data to.
        '''
        with open(file) as f:
            original_data: dict = json.load(f)
        
        modified_data = original_data | data # add data to original_data. Information in data will override original

        with open(file, "w") as f:
            f.write(json.dumps(modified_data, indent=indent))
            
    @staticmethod
    def clearfile(file: str = "user-data.json"):
        """Resets json files

        Paramters:
        ----------
            file (str, optional): file path and file. Defaults to "user-data.json".

        Raises:
        -------
            TypeError: file must be a .json file
        """        
        if file[-5:] != ".json":
            raise TypeError(f"Invalid file\nExpected file to end in .json. Instead it ended with \"{file[-5:]}\"")
        with open(file, "w") as f:
            f.write("{}")
    
    @staticmethod
    def clearfiles(files: tuple[str]=files):
        """wrapper for doing:
        ```
        for file in files:
            jsonUtils.clearfile(file=file)
        ```

        Parameters:
        ----------
            files (tuple[str], optional): an iterable of file names to clear. Defaults to ("preferences.json", "user-data.json").
        """        
        for file in files:
            jsonUtils.clearfile(file=file)
    
    
    @staticmethod
    def get(file: StringIO, sentinal: str|int, *, func: Callable = lambda: None) -> bool:
        """
        Search a json file for a string or int as a key. If found, call func() and return True. Otherwise, return False.

        Parameters:
        -----------
            file (StringIO): the file to be searched
            sentinal (str | int): The object to look for
            func (_type_, optional): The function to be called if the argument is found. 
                Must take value of file[sentinal] as first parameter. Defaults to lambda: None.

        Returns:
            bool: Whether or not the file was found
        
        Example Usage:
        --------------
        ```
        with open("names.json") as f:
            jsonUtils.get(f, "Bob", func=lambda name: print(name, " is famous!"))
        ```
        """        
        data: dict = json.load(file)
        if data.get(sentinal, False):
            func(data.get(sentinal))
            return True
        return False

    @staticmethod
    def get_values():
        """Get all user preferences and user conditions as an instance of class UserInfo

        Returns:
        --------
            UserInfo: dataclass containing conditions and preferances in the preferences.json and user-data.json files
        
        Example Usage:
        ------------
        ```
        data = jsonUtil.get_values()
        print(data)
        print(data.conditions)
        print(data.preferences)
        ```
        """        
        with open("preferences.json") as pref, open("user-data.json") as user_data:
            prefs, data = json.load(pref), json.load(user_data)
            
        return UserInfo(
            conditions=data.get("conditions", []),
            preferences={preference: prefs.get(preference) for preference in preferences}
            )


def main():
    j = jsonUtils
    j.clearfile()
    j.add({"conditions": ["asthma", "cancer"]})
    print(j.get_values())
            

if __name__ == "__main__":         
    main()
    