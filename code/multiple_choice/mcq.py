import tkinter as tk
import customtkinter as ctk
from dataclasses import dataclass

@dataclass
class Question:
    question: str
    answers: list[str]
    correct_answer: int | None

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
        for question in self.questions:
            self.__create_question(question)
            self.clean()
            if scored_quiz:
                score.append(self.correct)
        return score if scored_quiz else None
    
    def __create_question(self, question: Question, **kwargs):
        answers: list[str] = question.answers
        
        q = ctk.CTkLabel(
            self.root,
            text=question.question,
            font=kwargs.get("question_font", ("DEFAULT", 50))
        )
        q.pack()
        
        option = tk.IntVar(value=1) # what option number they chose
        
        for num, answer in enumerate(answers):
            var = tk.BooleanVar(value=True)
            
            
            def swap_selected(answer_selected = var): # for visual effect
                answer_selected.set(not answer_selected.get())
                
            
            button = ctk.CTkRadioButton(
                self.root,
                text=answer,
                variable=option,
                value=num+1,
                command=swap_selected
                )

            button.pack(pady=10)
        
        def leave():
            self.root.quit()
            print(option.get())
            print(option.get()==question.correct_answer)
            self.correct = (option.get()==question.correct_answer)
        
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
        (Question("What is 1+1", ["1", "2", "3"], 2)),
        Question("What is 2+2", ["1", "3", "7", "4"], 4)
        )
    mcq.begin()
    

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    main()
        