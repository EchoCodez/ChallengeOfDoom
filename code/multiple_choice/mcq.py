import tkinter as tk
import customtkinter as ctk
import typing
from dataclasses import dataclass, field

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
    
    

class MCQbuiler:
    def __init__(self, root: ctk.CTk, name, *questions: Question) -> None:
        self.questions = questions
        self.root = root
        self.name = name
        self.correct = False
    
    def clean(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def start(self, title_font= ("DEFAULT", 50), continue_font=("DEFAULT", 30), **kwargs):
        width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("{0}x{1}+0+0".format(width, height))
        
        ctk_title = ctk.CTkLabel(
            self.root,
            text=self.name,
            font=title_font
        )
        next_button = ctk.CTkButton(
            self.root,
            text="Start",
            font=continue_font,
            command=self.root.quit
        )
        
        ctk_title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        next_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.root.mainloop()
    
    def start_questions(self, scored_quiz = False) -> list[bool] | None:
        score = []
        corrects = []
        for question in self.questions:
            if isinstance(question, Question):
                self.__create_question(question)
            elif isinstance(question, CustomQuestion):
                question.question(*question.args, **question.kwargs)
            else:
                raise TypeError("Invalid Question {0}".format(question))
            
            self.clean()
            
            if scored_quiz:
                corrects.append(self.correct==question.correct_answer)
            else:
                score.append(self.correct)
        return corrects if scored_quiz else score
    
    def __create_question(self, question: Question, **kwargs):
        answers: list[str] = question.answers
        
        q = ctk.CTkLabel(
            self.root,
            text=question.question,
            font=kwargs.get("question_font", ("DEFAULT", 50))
        )
        q.pack()
        
        option = tk.StringVar() # what option they chose
        
        for answer in answers:
            button = ctk.CTkRadioButton(
                self.root,
                text=answer,
                variable=option,
                value=answer
                )

            button.pack(pady=10)
        
        def leave():
            self.root.quit()
            print(option.get())
            self.correct = (option.get())
        
        next_button = ctk.CTkButton(
            self.root,
            text="Continue",
            command=leave
        )
        
        next_button.pack(pady=10)

        self.root.mainloop()
        
        
        
    
    def end(self):
        pass
    
    def begin(self, **kwargs):
        self.start(**kwargs)
        self.clean()
        self.start_questions(**kwargs)
        self.end(**kwargs)
        
        
        
def main():
    mcq = MCQbuiler(
        ctk.CTk(),
        "My MCQ Test",
        (Question("Are you male or female?", ["Male", "Female", "Other"])),
        Question("What is 2+2?", ["1", "3", "7", "4"])
        )
    mcq.begin()
    

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    main()
        