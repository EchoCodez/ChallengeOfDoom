import tkinter as tk
import customtkinter as ctk
from logging import Logger
from utils.data_classes import Question, CustomQuestion
from utils.generic import UseLogger

class MCQbuiler(UseLogger):
    '''Builds a multiple choice quiz, with support for other types of questions. Container for questions.'''
    def __init__(
        self,
        root: ctk.CTk,
        name: str,
        logger: Logger,
        *questions: Question | CustomQuestion,
        include_start: bool = True,
        include_end: bool = True,
        ) -> None:
        """Initialize Multiple Choice Quiz

        Parameters:
        -----------
            root (ctk.CTk): customtkinter root
            name (str): Name of test
            
            include_start (bool, kwarg, optional): Whether to create a start screen. Defaults to True.
            
            include_end (bool, kwarg, optional): Whether to create an end screen. Defaults to True.
            
        Raises:
        -------
            TypeError: All questions must be instances of Question or CustomQuestion
        """
        
        if not all(isinstance(q, (Question, CustomQuestion)) for q in questions):
            raise TypeError("All questions must be instances of Question or CustomQuestion")
        
        super().__init__(logger)
        self.questions = questions
        self.iterator = (i for i in self.questions)
        self.root = root
        self.name = name
        self.include_start = include_start
        self.include_end = include_end
    
    def clean(self):
        """Remove all widgets from the screen
        """
        
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def _start(self, title_font= ("DEFAULT", 50), continue_font=("DEFAULT", 30), **kwargs):
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
    
    def _start_questions(self, scored_quiz = False, **kwargs) -> list[bool] | list[str]:
        """Wrapper for iterating through and creating questions

        Parameters:
        -----
            scored_quiz (bool, optional): Whether or not to score the quiz. Defaults to False.

        Raises:
        -------
            TypeError: If question is not instance of Question or CustomQuestion

        Returns:
        --------
            `list[bool] | list[str]`: list of correct and incorrect answers | list of user results as strings
        """
        
        self.results = [None] * len(self)
        self._index = 0
        while self._index < len(self):
            
            question = self[self._index]
            
            if isinstance(question, Question):
                self._create_question(question)
            elif isinstance(question, CustomQuestion):
                self.answer = question.question(*question.args, **question.kwargs)
            elif question() is not None:
                raise TypeError("Invalid Question {0}".format(question))
            
            self.clean()
            self._index+=1
            
            if self.answer is not None:
                self.results[self._index] = self.answer
                
        return [x==q.correct_answer for x, q in zip(self.results, self)] if scored_quiz else self.results
    
    def _create_question(self, question: Question, **kwargs):
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
        q.pack(pady=kwargs.get("question_pady", 100))
        
        option = tk.StringVar(value=answers[0]) # what option they chose
        
        for answer in answers:
            button = ctk.CTkRadioButton(
                self.root,
                text=answer,
                variable=option,
                value=answer
                )

            button.pack(pady=20)
        
        def leave():
            self.logger.debug(f"User choose option {option.get()}")
            self.answer = option.get()
            self.root.quit()
        
        def back():
            self.logger.debug("User went back a page")
            self.answer = None
            self._index-=2
            self.root.quit()
        
        next_button = ctk.CTkButton(
            self.root,
            text="Continue",
            command=leave
        )
        
        next_button.place(relx=0.8, rely=0.8, anchor=tk.CENTER)

        if self._index:
            ctk.CTkButton(
                self.root,
                text="Back",
                command=back
            ).place(relx=0.2, rely=0.8, anchor = tk.CENTER)

        self.root.mainloop()
        
        
    def _end(
        self,
        title_next="The End!",
        continue_text = "Finish",
        title_font= ("DEFAULT", 50),
        continue_font=("DEFAULT", 30),
        next_button_width: int = 140,
        next_button_height: int = 28,
        **kwargs
        ) -> None:
        """Creates the end screen of quiz

        Parameters:
        -----------
            title_next (str, optional): Title of the ending screen. Defaults to "The End!".
            
            continue_text (str, optional): Finish button text. Defaults to "Finish".
            
            title_font (tuple, optional): Font options for title. Defaults to `("DEFAULT", 50)`.
            
            continue_font (tuple, optional): Font options for button. Defaults to `("DEFAULT", 30)`.
            
            next_button_width (int, optional): height of next button on end screen. Defaults to 140
            
            next_button_height (int, optional): height of next button on end screen. Defaults to 28
        """
        self.logger.debug("ended")
        
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
            command=self.root.quit,
            width=next_button_width,
            height=next_button_height
        )
        
        ctk_title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        next_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.root.mainloop()
    
    def begin(self, **kwargs):
        """Wrapper for creating start screen, going through questions, and creating end screen
        """        
        if self.include_start:
            self._start(**kwargs)
            
        self.logger.debug("Started Quiz")
        self.clean()
        
        answers = self._start_questions(**kwargs)
        self.clean()
        
        self.logger.debug("Cleaned")
        
        if self.include_end:
            self._end(**kwargs)
        else:
            self.clean()
        
        self.logger.debug("Ended Quiz")
        
        return answers
        
    def __iter__(self) -> list[Question | CustomQuestion]:
        return self.questions.__iter__()
    
    def __getitem__(self, *args) -> Question | CustomQuestion:
        return self.questions.__getitem__(*args)
        
    def __len__(self) -> int:
        return self.questions.__len__()