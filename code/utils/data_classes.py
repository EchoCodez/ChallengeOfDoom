import dataclasses
import typing
import itertools as it

from apscheduler.job import Iterable
import utils.parse_json as jsonUtils
from utils.constants import TODAY, BODY_LOCATIONS

__all__ = (
    "Question",
    "CustomQuestion",
    "UserInfo",
    "ActionButton",
    "InformationSheet",
    "SettingsAttr",
    "WeatherInfo",
    "BodyParts",
    "Symptoms"
)

@dataclasses.dataclass(frozen=True, slots=True)
class Question:
    """A Question for the Multiple Choice Quiz Builder
    
    Parameters:
    -----------
        question (str): The Question title. Ex) "What is 1+1?"
        
        answers (Iterable[str]): A list of the multiple choice question answers
        
        correct_answer (int, None, optional): The index correct answer (starting index is 1). 
        Defaults to None, meaning it is a survey question
            
    Raises:
    -------
        `FrozenInstanceError`: parameters are modified after creation
    """    
    question: str
    answers: typing.Iterable[str]
    correct_answer: int | None = None

    def __str__(self):
        return f"Question {self.question}"
    
@dataclasses.dataclass(frozen=True, slots=True)
class CustomQuestion:
    '''A Custom question. Results from the custom requestion must be stored from within the callable.
    If possible, writing to file should be done inside function. Otherwise if return value is not None,
    it will add the return value to the list of answers return at the end of `MCQbuilder.begin()`
    
    Parameters:
    -----------
        question (`Callable`): A method or function that can be called to create the question
        
        args (`Iterable`): Iterable of question arguments. Defaults to `()`
        
        kwargs (`dict`): kwargs for question. Defaults to `dict()`
        
    Raises:
    -------
        `FrozenInstanceError`: parameters are modified after creation
    '''
    
    question: typing.Callable
    args: typing.Iterable = dataclasses.field(default_factory=tuple)
    kwargs: dict = dataclasses.field(default_factory=dict)
    
    def __str__(self):
        return f"CustomQuestion {self.question.__name__}"

@dataclasses.dataclass(frozen=True, slots=True)
class UserInfo:
    '''Dataclass storing information about user and user preferences'''
    
    conditions: list[str]
    preferences: dict[str, bool|str]
    gender: str
    birthyear: str
    api_username: str
    api_password: str

    @property
    def selector_status(self) -> typing.Literal["man", "woman", "boy", "girl"]:
        is_adult = (TODAY.year-int(self.birthyear)) >= 18
        
        if is_adult:
            return "man" if self.gender.lower() == "male" else 'woman'
        else:
            return "boy" if self.gender.lower() == "male" else "girl"

@dataclasses.dataclass(frozen=True, slots=True)
class ActionButton:
    text: str
    command: typing.Callable
    kwargs: dict = dataclasses.field(default_factory=dict)

@dataclasses.dataclass(frozen=True, slots=True)
class InformationSheet:
    """Class containing data needed for the InformationPages constructor
    
    Parameters:
    -----------
        title (str): Title of the page
        
        content (str): Content shown on that page
        
        buttons (Iterable[ActionButton], optional): The buttons to be added on each page. Defautls to empty tuple.
    """    
    title: str
    content: str
    buttons: typing.Iterable[ActionButton] = dataclasses.field(default_factory=tuple)
    button_pack_kwargs: dict = dataclasses.field(default_factory=dict)

@dataclasses.dataclass(frozen=True, slots=True)
class SettingsAttr:
    """An Attribute for settings
    
    Parameters:
    -----------
        name (str): Name of label
        
        command (Callable): What to do when button is clicked
        
        kwargs (dict, optional): kwargs to be passed in to constructer when creating setting
    """    
    name: str
    command: typing.Callable
    kwargs: dict = dataclasses.field(default_factory=dict)

    def __iter__(self):
        return (self.name, self.command, self.kwargs).__iter__()


@dataclasses.dataclass
class WeatherInfo:
    """Class storing weather and pollen info
    """    
    grass_pollen: int
    tree_pollen: int
    weed_pollen: int
    grass_pollen_risk: float
    tree_pollen_risk: float
    weed_pollen_risk: float
    
class BodyParts:
    def __init__(self, *parts: str) -> None:
        self.parts = {x.title() for x in parts}

    def subparts_to_ids(self) -> tuple[int]:
        data = it.chain(*[d["sublocations"] for d in jsonUtils.read(BODY_LOCATIONS)])
        return tuple(d["ID"] for d in data if d["Name"].title() in self) # type: ignore
        
    def __iadd__(self, item: typing.Iterable[str]):
        item = tuple(item) 
        if not all(isinstance(x, str) for x in item):
            raise TypeError("All items must be of class str")
        self.parts = {*self.parts, *(x.title() for x in item)}
        return self

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.parts)
    
    # implement for efficiency
    def __contains__(self, arg: typing.Any) -> bool:
        return arg in self.parts
                
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(self.parts)})"


class Symptoms:
    def __init__(self, subparts: BodyParts) -> None:
        self._symptoms = {part: self.get_id_by_subpart(part) for part in subparts}

    @staticmethod
    def get_id_by_subpart(subpart: str):
        for d in jsonUtils.read(BODY_LOCATIONS):
            for part in d["subparts"]:
                if subpart == part["Name"]:
                    return part["ID"]

        raise ValueError(f"{subpart} not found!")

    def __getitem__(self, *args: typing.Any):
        return self._symptoms.__getitem__(*args)

    def __delitem__(self, *args: typing.Any):
        return self._symptoms.__delitem__(*args)

    def __str__(self) -> str:
        return f"{type(self).__name__}({', '.join(self._symptoms)})"

    def __iadd__(self, __o: Iterable[str] | str):
        if isinstance(__o, Iterable):
            self._symptoms.update({x: self.get_id_by_subpart(x) for x in __o})
        else:
            self._symptoms[str(__o)] = self.get_id_by_subpart(__o)
        return self
        


