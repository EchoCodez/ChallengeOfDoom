import json
import os
from typing import Callable
from io import StringIO
from utils.data_classes import UserInfo



preferences = ("appearance_theme", "save_data")
files = ("json/preferences.json", "json/user-data.json")


class jsonUtils:
    '''Class containing custom made json file methods'''
    __slots__ = ()

    @staticmethod
    def add(data: dict, file: str = "json/user-data.json", indent=4) -> None:
        '''
        Adds data to a file
        
        Parameters
        ----------
        data (dict): The data to be added
        
        file (str, optional): "user-data.json"
            Which file to add data to.
        '''

        new_data = jsonUtils.open(file) | data
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(new_data, indent=indent))

    @staticmethod
    def write(data: dict, file: str = "json/user-data.json", indent=4) -> None:
        '''
        Adds data to a file
        
        Parameters
        ----------
        data (dict | list): The data to be added
        
        file (str, optional): "user-data.json"
            Which file to add data to.
        '''
        
        with open(file, encoding="utf-8") as f:
            original_data: dict | list = json.load(f)
        
        if isinstance(original_data, dict) and isinstance(data, dict):
            modified_data = original_data | data # add data to original_data. Information in data will override original
        elif isinstance(original_data, dict) and isinstance(data, dict):
            raise TypeError("Cannot add dict to list inside json file")
        elif isinstance(original_data, list) and isinstance(data, list):
            original_data.append(data)
            modified_data = original_data
        elif isinstance(modified_data, list) and isinstance(data, dict):
            modified_data = original_data+[data]
        else:
            raise TypeError(
                "Invalid argument type of {0} for json file data, and {1} for data parameter".format(
                    type(original_data), type(data)
                    )
                )

        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(modified_data, indent=indent))
            
    @staticmethod
    def clearfile(file: str = "json/user-data.json") -> None:
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
        with open(file, "w", encoding="utf-8") as f:
            f.write("{}")
    
    @staticmethod
    def clearfiles(files: tuple[str]=files, clearlogs = False) -> None:
        """wrapper for doing:
        ```
        for file in files:
            jsonUtils.clearfile(file=file)
            
        if clearlogs:
            for log in jsonUtils.read("json/logs.json")["logs_list"]:
                jsonUtils.delete_file(log)
            jsonUtils.overwrite({"logs_list": []}, file="json/logs.json")
        ```

        Parameters:
        ----------
            files (tuple[str], optional): an iterable of file names to clear. Defaults to ("preferences.json", "user-data.json").\n
            clearlogs (bool, optional): clear old health diagnosis logs. Defaults to False.
        """
            
        for file in files:
            jsonUtils.clearfile(file=file)
            
        if clearlogs:
            for log in jsonUtils.read("json/logs.json")["logs_list"]:
                jsonUtils.delete_file(log)
            jsonUtils.overwrite({"logs_list": []}, file="json/logs.json")
    
    @staticmethod
    def get(file: StringIO, sentinal: str|int, *, func: Callable = lambda x: None) -> bool:
        """
        Search a json file for a string or int as a key. If found, call func() and return True. Otherwise, return False.

        Parameters:
        -----------
            file (StringIO): the file to be searched
            sentinal (str | int): The object to look for
            func (Callable, optional): The function to be called if the argument is found. 
                Must take value of file[sentinal] as first parameter. Defaults to lambda x: None.

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
    def get_values() -> UserInfo:
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
        
        prefs, data = jsonUtils.open("json/preferences.json"), jsonUtils.open("json/user-data.json")
        
        return UserInfo(
            conditions=data.get("conditions", []),
            preferences={preference: prefs.get(preference) for preference in preferences},
            gender=data.get("gender"),
            birthyear=data.get("birth_year"),
            api_username=data.get("api_username", ""),
            api_password=data.get("api_password", "")
            )
    
    @staticmethod
    def open(file: str) -> list[dict] | dict:
        """returns the json loaded file of a file path

        Parameters:
        -----------
            file (str): file path
        
        Returns:
        --------
        list[dict]: a list containing all entries in the json file as dictionaries
        
        Implementation:
        ---------------
        ```
        with open(file) as f:
            return json.load(f)
        ``` 
        """
          
        with open(file, encoding="utf-8") as f:
            return json.load(f)
        
    @staticmethod
    def search(file: str, sentinal: int, **kwargs) -> str | dict:
        '''
        Search for a given string in a json file
        
        Parameters:
        -----------
        file (`str`): the file path to the json file to search
        sentinal (`int`): The ID to search for
        kwargs (`dict[str, str]`, optional): Valid kwargs include "search_for", "return", and "return_dict".
            They default to "ID", "Name" and False respectively.
            See implementation for details on their function
        
        Raises:
        -------
        TypeError: Kwarg is not one of the listed kwargs
        
        Returns:
        --------
        str | dict: string if `symptom[kwargs[_return]]` is string, and dict if `kwargs[return_dict]` is True
        
        Example Use:
        ------------
        ```
        def look_for_id() -> str:
            ID = 9
            disease_name = jsonUtils.search(
                file = "json/symptoms.json",
                sentinal = ID
                )
            return disease_name

        def look_for_name() -> int:
            name="Bad Breath"
            disease_id = jsonUtils.search(
                file = "json/symptoms.json",
                sentinal = name,
                search_for = "Name",
                _return = "ID"
                )
            return disease_id
        
        def get_id_symptom():
            ID = 9
            symptom = jsonUtils.search(
                file = "json/symptoms.json",
                sentinal = ID,
                _return = "Name"
                )
            return symptom
        ```
        
        Implementation:
        ---------------
        ```
        @staticmethod
        def search(file: str, sentinal: int, **kwargs) -> str | dict:
            data = jsonUtils.open(file)
            search_for = kwargs.pop("search_for", "ID")
            return_dict = kwargs.pop("return_dict", False)
            _return = kwargs.pop("_return", "Name")
            
            if kwargs:
                raise TypeError("Unknown kwargs {0}".format(kwargs))
            
            if isinstance(data, dict):
                return data if return_dict else data[_return]
            
            for symptom in data:
                if symptom.get(search_for) == sentinal:
                    return symptom if return_dict else symptom[_return]
        ```
        '''
        
        data = jsonUtils.open(file)
        search_for = kwargs.pop("search_for", "ID")
        return_dict = kwargs.pop("return_dict", False)
        _return = kwargs.pop("_return", "Name")
        
        if kwargs:
            raise TypeError("Unknown kwargs {0}".format(kwargs))
        
        if isinstance(data, dict):
            return data if return_dict else data[_return]
        
        for symptom in data:
            if symptom.get(search_for) == sentinal:
                return symptom if return_dict else symptom[_return]
    
    @staticmethod
    def overwrite(data, file: str, *, dumps = True) -> None:
        """Overwrite data in a file

        Parameters:
        ----------
            data (dict | dumps): the data to overwrite the file with
            
            file (str): the file path
            
            dumps (bool, optional): whether to write `json.dumps(data)`. Defaults to True.
        """
            
        with open(file, "w", encoding="utf-8") as f:
            if dumps:
                f.write(json.dumps(data, indent=4))
            else:
                f.write(data)

    @staticmethod
    def read(file: str) -> dict | list[dict]:
        """Wrapper for jsonUtils.open

        Args:
            file (str): file path to json file

        Returns:
            dict | list[dict]: The json file
        """
        
        return jsonUtils.open(file)

    @staticmethod
    def open_json(path: str, action: str = "r") -> None:
        """Context manager for opening json files. 
        Instead of returning a file object, the object returned is a json.load(file) object. 
        This should mainly be used for readability

        Parameters:
        -----------
            path (`str`): Path to the file
            
            action (`str`, optional): What action to take with the file. Options include any of the parameters from open.
            
            Defaults to "r". If anything other than "r" is used, it returns the file object as well.

        Returns:
        --------
            `Any | tuple[Any, fp]`: json loaded version of file, or tuple of json loaded version of file and file object (only if `action != r`)
        """        
        return open_json(path, action)

    @staticmethod
    def delete_file(path: str) -> None:
        '''Deletes a file. If exception is thrown, catches it silently'''
        try:
            os.remove(path)
        except Exception:
            pass


class open_json:
    def __init__(self, path: str, action: str = "r") -> None:
        self.path = path
        self.action = action
        self.return_file = (self.action != "r")
    
    def __enter__(self):
        if self.return_file:
            self.file = open(self.path, self.action)
            return (json.load(self.file), self.file)
        
        with open(self.path, self.action, encoding="utf-8") as f:
            return json.load(f)
        
    
    def __exit__(self, exception_type, exception_value, traceback) -> None:
        if self.return_file:
            self.file.close()
    
