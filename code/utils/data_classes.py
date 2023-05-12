import dataclasses
import typing

@dataclasses.dataclass(frozen=True)
class Question:
    """A Question for the Multiple Choice Quiz Builder
    
    Parameters:
    -----------
        question (str): The Question title. Ex) What is 1+1?
        
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
    
@dataclasses.dataclass(frozen=True)
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
    args: typing.Iterable = ()
    kwargs: dict = dataclasses.field(default_factory=dict)
    
    def __str__(self):
        return f"CustomQuestion {self.question.__name__}"

@dataclasses.dataclass
class UserInfo:
    '''Dataclass storing information about user and user preferences'''
    
    conditions: list[str]
    preferences: dict[str, bool]
    gender: str
    birthyear: str
    
    def __iter__(self):
        return iter({
            "conditions": self.conditions,
            "preferences":self.preferences,
            "gender":self.gender,
            "birth_year":self.birthyear
            }.items())
    
    def __str__(self) -> str:
        x = '\n\t'.join(f"{k}={v}" for k, v in self)
        return f"{self.__class__.__name__}:\n\t{x}"
