import dataclasses
import typing

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

