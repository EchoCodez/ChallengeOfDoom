from __future__ import annotations

import json
from typing import Callable, Any
from io import StringIO
from utils.data_classes import UserInfo
from utils.constants import *


preferences = ("appearance_theme", "save_data")
files = (PREFERENCES, USER_DATA)


def add(data: dict, file: Path = USER_DATA, indent: int = 4) -> None:
    '''
    Adds data to a file
    
    Parameters
    ----------
    data (dict): The data to be added
    
    file (Path, optional): "user-data.json"
        Which file to add data to.
    '''
    new_data = read(file)
    if isinstance(new_data, list):
        raise TypeError(f"data in {file} must be a dictionary: try using ")
    new_data = new_data | data
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(new_data, indent=indent))

def write(data: dict, file: Path = USER_DATA, indent=4) -> None:
    '''
    Adds data to a file
    
    Parameters
    ----------
    data (dict | list): The data to be added
    
    file (Path, optional): "user-data.json"
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
        
def clearfile(file_path: Path = USER_DATA) -> None:
    """Resets json files

    Paramters:
    ----------
        file (Path, optional): file path and file. Defaults to "user-data.json".

    Raises:
    -------
        TypeError: file must be a .json file
    """
    
    if file_path.suffix != ".json":
        raise TypeError(f"Invalid file path\nExpected file to end in .json, not \"{file_path.suffix}\"")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("{}")

def clearfiles(files: tuple[Path] = files, clearlogs = False) -> None:
    """wrapper for doing:
    ```
    for file in files:
        clearfile(file=file)
        
    if clearlogs:
        for log in read(LOGS)["logs_list"]:
            delete_file(log)
        overwrite({"logs_list": []}, file=LOGS)
    ```

    Parameters:
    ----------
        files (tuple[Path], optional): an iterable of file names to clear. Defaults to ("preferences.json", "user-data.json").\n
        clearlogs (bool, optional): clear old health diagnosis logs. Defaults to False.
    """
        
    for file in files:
        clearfile(file)
        
    if clearlogs:
        for log in HEALTH_LOGS.iterdir():
            delete_file(log)

def get(file: StringIO, sentinal: str|int, *, func: Callable[[Any], None] = lambda _: None) -> bool:
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
    if isinstance(data, dict):
        if data.get(sentinal, False):
            func(data.get(sentinal))
            return True
    else:
        raise ValueError(f"data in file must be a dictionary: got {type(data).__name__} instead")
    return False

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
    
    prefs, data = read(PREFERENCES), read(USER_DATA)
    
    return UserInfo(
            conditions=data.get("conditions", []),
            preferences={preference: prefs.get(preference) for preference in preferences},
            gender=data.get("gender"),
            birthyear=data.get("birth_year"),
            api_username=data.get("api_username", ""),
            api_password=data.get("api_password", "")
        )

def read(file: Path) -> list[dict] | dict:
    """returns the json loaded file of a file path

    Parameters:
    -----------
        file (Path): file path
    
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
    
def search(file: Path, sentinal: int, **kwargs) -> str | dict:
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
        disease_name = search(
            file = "json/symptoms.json",
            sentinal = ID
            )
        return disease_name

    def look_for_name() -> int:
        name="Bad Breath"
        disease_id = search(
            file = "json/symptoms.json",
            sentinal = name,
            search_for = "Name",
            _return = "ID"
            )
        return disease_id
    
    def get_id_symptom():
        ID = 9
        symptom = search(
            file = "json/symptoms.json",
            sentinal = ID,
            _return = "Name"
            )
        return symptom
    ```
    
    Implementation:
    ---------------
    ```

    def search(file: str, sentinal: int, **kwargs) -> str | dict:
        data = read(file)
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
    
    data = read(file)
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

def overwrite(data: dict | list, file: Path, *, dumps = True) -> None:
    """Overwrite data in a file

    Parameters:
    ----------
        data (dict | dumps): the data to overwrite the file with
        
        file (Path): the file path
        
        dumps (bool, optional): whether to write `json.dumps(data)`. Defaults to True.
    """
        
    with open(file, "w", encoding="utf-8") as f:
        if dumps:
            f.write(json.dumps(data, indent = 4))
        else:
            f.write(str(data))

def open_json(path: Path, action: str = "r", **kwargs) -> OPEN_JSON:
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
    return OPEN_JSON(path, action, kwargs)

def delete_file(path: Path) -> None:
    '''Deletes a file. If exception is thrown, catches it silently'''
    if not isinstance(path, Path):
        raise TypeError(
            f"path must be an instance of {type(Path).__name__}"
            f"Try passing in Path({path}) instead" if isinstance(path, str) else ''
            )
    path.unlink()


class OPEN_JSON:
    '''Context manager for opening json files'''
    def __init__(self, path: str, action: str = "r", kwargs: dict[str, Any] = None) -> None:
        self.path = path
        self.action = action
        self.return_file = ("r" not in self.action)
        self.kwargs = kwargs
    
    def __enter__(self):
        if self.return_file:
            self.file = open(self.path, self.action, encoding="utf-8", **self.kwargs)
            return (json.load(self.file), self.file)
        
        with open(self.path, self.action, encoding="utf-8") as f:
            return json.load(f)
        
    
    def __exit__(self, exception_type, exception_value, traceback) -> None:
        if self.return_file:
            self.file.close()
    
