from dataclasses import dataclass, field
import typing

@dataclass
class Question:
    """A Question for the Multiple Choice Quiz Builder
    
    Parameters:
    -----------
        question (str): The Question title. Ex) What is 1+1?
        
        answers (Iterable[str]): A list of the multiple choice question answers
        
        correct_answer (int, None, optional): The index correct answer (starting index is 1). Defaults to None, meaning it is a survey question
    """    
    question: str
    answers: typing.Iterable[str]
    correct_answer: int | None = None
    
@dataclass
class CustomQuestion:
    '''A Custom question
    
    Parameters:
    -----------
        question (`Callable`): A method or function that can be called to create the question
        
        args (`Iterable`): Iterable of question arguments. Defaults to `tuple()`
        
        kwargs (`dict`): kwargs for question. Defaults to `dict()`
    '''
    
    question: typing.Callable
    args: typing.Iterable = ()
    kwargs: dict = field(default_factory=dict)