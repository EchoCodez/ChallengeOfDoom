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
        """Initialize Multiple Choice Quiz

        Parameters:
        -----------
            root (ctk.CTk): customtkinter root
            
            name (_type_): Name of test
        """
        
        self.questions = questions
        self.root = root
        self.name = name
        self.correct = False
    
    def clean(self):
        """Remove all widgets from the screen
        """
        
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def start(self, title_font= ("DEFAULT", 50), continue_font=("DEFAULT", 30), **kwargs):
        """Creates the start page of the quiz

        Parameters:
        -----------
            title_font (tuple, optional): Font of the quiz title. Defaults to ("DEFAULT", 50).
            
            continue_font (tuple, optional): Font options of the continue button. Defaults to ("DEFAULT", 30).
        """
        
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
    
    def start_questions(self, scored_quiz = False) -> list[bool] | list[str]:
        """Wrapper for iterating through and creating questions

        Parameters:
        -----
            scored_quiz (bool, optional): Whether or not to score the quiz. Defaults to False.

        Raises:
        -------
            TypeError: If question is not instance of Question or CustomQuestion

        Returns:
        --------
            list[bool] | list[str]: list of correct and incorrect answers | list of user results as strings
        """
        
        score = []
        corrects: list[bool] = []
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
        """Creates question if `isinstance(question, Question)`

        Parameters:
        -----------
            question (Question): The question
        """
        
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
        
        
        
    
    def end(self, title_next="The End!", continue_text = "Finish", title_font= ("DEFAULT", 50), continue_font=("DEFAULT", 30), **kwargs):
        """Creates the end screen of quiz

        Parameters:
        -----------
            title_next (str, optional): Title of the ending screen. Defaults to "The End!".
            
            continue_text (str, optional): Finish button text. Defaults to "Finish".
            
            title_font (tuple, optional): Font options for title. Defaults to ("DEFAULT", 50).
            
            continue_font (tuple, optional): Font options for button. Defaults to ("DEFAULT", 30).
        """        
        
        width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("{0}x{1}+0+0".format(width, height))
        
        ctk_title = ctk.CTkLabel(
            self.root,
            text=title_next,
            font=title_font
        )
        next_button = ctk.CTkButton(
            self.root,
            text=continue_text,
            font=continue_font,
            command=self.root.quit
        )
        
        ctk_title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        next_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.root.mainloop()
    
    def begin(self, **kwargs):
        """Wrapper for creating start screen, going through questions, and creating end screen
        """        
        
        self.start(**kwargs)
        self.clean()
        self.start_questions(**kwargs)
        self.clean()
        self.end(**kwargs)
        
        
        
def main():
    """Testing/Debugging function
    """
    
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
        