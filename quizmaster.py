import tkinter as tk
from tkinter import messagebox


# ==========================================
# QUESTIONS AND ANSWERS
# ==========================================

questions = [
    {
        "question": "What is 2 + 2?",
        "answer": "4"
    },
    {
        "question": "Capital of Japan?",
        "answer": "Tokyo"
    },
    {
        "question": "How many days in a week?",
        "answer": "7"
    }
]


# ==========================================
# GUI QUIZ AGENT
# ==========================================

class QuizAgent:

    def __init__(self, root):

        self.root = root
        self.root.title("Smart Quiz Agent")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Quiz variables
        self.player = ""
        self.score = 0
        self.current_question = 0

        # ==================================
        # TITLE
        # ==================================

        self.title_label = tk.Label(
            root,
            text="🧠 SMART QUIZ AGENT",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=25)

        # ==================================
        # PLAYER NAME
        # ==================================

        self.name_label = tk.Label(
            root,
            text="Enter your name:",
            font=("Arial", 14)
        )
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(
            root,
            font=("Arial", 14),
            width=30
        )
        self.name_entry.pack(pady=10)

        # ==================================
        # START BUTTON
        # ==================================

        self.start_button = tk.Button(
            root,
            text="Start Quiz",
            font=("Arial", 14, "bold"),
            command=self.start_quiz,
            width=15
        )
        self.start_button.pack(pady=20)

        # ==================================
        # QUESTION LABEL
        # ==================================

        self.question_label = tk.Label(
            root,
            text="",
            font=("Arial", 17, "bold"),
            wraplength=500
        )

        # ==================================
        # QUESTION NUMBER
        # ==================================

        self.question_number_label = tk.Label(
            root,
            text="",
            font=("Arial", 12)
        )

        # ==================================
        # ANSWER BOX
        # ==================================

        self.answer_entry = tk.Entry(
            root,
            font=("Arial", 15),
            width=35
        )

        # ==================================
        # SUBMIT BUTTON
        # ==================================

        self.submit_button = tk.Button(
            root,
            text="Submit Answer",
            font=("Arial", 13, "bold"),
            command=self.check_answer,
            width=18
        )

        # ==================================
        # FEEDBACK
        # ==================================

        self.feedback_label = tk.Label(
            root,
            text="",
            font=("Arial", 13, "bold")
        )

        # ==================================
        # RESULT
        # ==================================

        self.result_label = tk.Label(
            root,
            text="",
            font=("Arial", 18, "bold"),
            wraplength=500
        )

        # ==================================
        # RESTART BUTTON
        # ==================================

        self.restart_button = tk.Button(
            root,
            text="Restart Quiz",
            font=("Arial", 13, "bold"),
            command=self.restart_quiz,
            width=15
        )

        # ==================================
        # EXIT BUTTON
        # ==================================

        self.exit_button = tk.Button(
            root,
            text="Exit",
            font=("Arial", 13, "bold"),
            command=root.destroy,
            width=15
        )


    # ==========================================
    # START QUIZ
    # ==========================================

    def start_quiz(self):

        self.player = self.name_entry.get().strip()

        if self.player == "":
            messagebox.showwarning(
                "Name Required",
                "Please enter your name first."
            )
            return

        # Reset quiz
        self.score = 0
        self.current_question = 0

        # Hide starting widgets
        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()

        # Show quiz widgets
        self.question_number_label.pack(pady=5)
        self.question_label.pack(pady=20)
        self.answer_entry.pack(pady=10)
        self.submit_button.pack(pady=15)
        self.feedback_label.pack(pady=10)

        # Show first question
        self.show_question()


    # ==========================================
    # SHOW QUESTION
    # ==========================================

    def show_question(self):

        # Check if quiz is finished
        if self.current_question >= len(questions):
            self.finish_quiz()
            return

        question = questions[self.current_question]["question"]

        self.question_number_label.config(
            text=f"Question {self.current_question + 1} of {len(questions)}"
        )

        self.question_label.config(
            text=question
        )

        # Clear previous answer
        self.answer_entry.delete(0, tk.END)

        self.feedback_label.config(
            text=""
        )

        # Put cursor in answer box
        self.answer_entry.focus()


    # ==========================================
    # CHECK ANSWER
    # ==========================================

    def check_answer(self):

        user_answer = self.answer_entry.get().strip()

        if user_answer == "":
            messagebox.showwarning(
                "Answer Required",
                "Please enter an answer."
            )
            return

        correct_answer = questions[
            self.current_question
        ]["answer"]

        # Compare answers
        if user_answer.lower() == correct_answer.lower():

            self.feedback_label.config(
                text="✅ Correct!",
                fg="green"
            )

            self.score += 1

        else:

            self.feedback_label.config(
                text=f"❌ Wrong! Correct answer: {correct_answer}",
                fg="red"
            )

        # Move to next question
        self.current_question += 1

        # Wait before showing next question
        self.root.after(1000, self.show_question)


    # ==========================================
    # FINISH QUIZ
    # ==========================================

    def finish_quiz(self):

        # Hide quiz widgets
        self.question_number_label.pack_forget()
        self.question_label.pack_forget()
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.feedback_label.pack_forget()

        # Show result
        self.result_label.pack(pady=40)

        result_text = (
            f"🎉 Quiz Over!\n\n"
            f"Player: {self.player}\n"
            f"Score: {self.score} / {len(questions)}\n\n"
        )

        # Feedback
        if self.score == len(questions):

            result_text += "🏆 Perfect score! Amazing!"

        elif self.score >= len(questions) / 2:

            result_text += "👏 Good job!"

        else:

            result_text += "📚 Keep practising — you will get there!"

        self.result_label.config(
            text=result_text
        )

        # Save score
        self.save_score()

        # Show buttons
        self.restart_button.pack(pady=10)
        self.exit_button.pack(pady=5)


    # ==========================================
    # SAVE SCORE
    # ==========================================

    def save_score(self):

        with open("scores.txt", "a") as file:

            file.write(
                self.player
                + " scored "
                + str(self.score)
                + " out of "
                + str(len(questions))
                + "\n"
            )


    # ==========================================
    # RESTART QUIZ
    # ==========================================

    def restart_quiz(self):

        self.score = 0
        self.current_question = 0

        # Hide result and buttons
        self.result_label.pack_forget()
        self.restart_button.pack_forget()
        self.exit_button.pack_forget()

        # Show name screen
        self.name_label.pack(pady=5)
        self.name_entry.pack(pady=10)
        self.start_button.pack(pady=20)

        # Clear name
        self.name_entry.delete(0, tk.END)


# ==========================================
# RUN APPLICATION
# ==========================================

root = tk.Tk()

quiz = QuizAgent(root)

root.mainloop()