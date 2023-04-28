import tkinter as tk
import customtkinter as ctk
from dataclasses import dataclass

@dataclass
class Question:
    question: str
    answers: list[str]
    correct_answer: int

@dataclass
class Answer:
    text: str
    is_correct: bool = False

class MCQbuiler:
    def __init__(self, root: ctk.CTk, name, *questions: Question) -> None:
        self.questions = questions
        self.root = root
        self.name = name
    
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
    
    def start_questions(self):
        for question in self.questions:
            self.__create_question(question)
    
    def __create_question(self, question: Question, **kwargs):
        answers: list[str] = question.answers
        
        q = ctk.CTkLabel(
            self.root,
            text=question.question,
            font=kwargs.get("question_font", ("DEFAULT", 50))
        )
        q.pack()
        
        screen_answers = [None]*len(answers)
        selected_vars = [None]*len(answers)
        for num, answer in enumerate(answers):
            answer_selected = tk.BooleanVar(value=True)
            
            def swap_selected(answer_selected = answer_selected):
                answer_selected.set(True)
                
            
            screen_answers[num] = ctk.CTkRadioButton(
                self.root,
                text=answer,
                value=False,
                command=swap_selected
                )

            screen_answers[num].pack(pady=10)
            selected_vars[num] = answer_selected
            
        def restart():
            self.clean()
            self.__create_question(question, **kwargs)
        
        def leave():
            self.root.quit()
            self.result = [a.get() for a in selected_vars]
            print(self.result)
        
        next_button = ctk.CTkButton(
            self.root,
            text="Continue",
            command=leave
        )
        
        clear_button = ctk.CTkButton(
            self.root,
            text="clear",
            command=restart
        )
        
        next_button.pack(pady=10)
        clear_button.pack(pady=10)
        #TODO: Raise GUI warning if user tries to enter more than 1 answer

        self.root.mainloop()
        
        
        
    
    def end(self):
        pass
    
    def begin(self, **kwargs):
        self.start(**kwargs)
        self.clean()
        self.start_questions(**kwargs)
        self.end(**kwargs)
        
        
        
def main():
    mcq = MCQbuiler(ctk.CTk(), "My MCQ Test", (Question("What is 1+1", ["1", "2", "3"], 2)))
    mcq.begin()
    

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    main()
        