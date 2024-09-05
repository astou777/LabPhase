import tkinter as tk
from tkinter import messagebox
import json

def cleanup():
    """Gère le nettoyage des ressources."""
    print("Nettoyage terminé.")

def run_quiz_app():
    """Instancie la classe Quiz et exécute l'application GUI."""
    with open('C:/Users/DELL/Desktop/fichier_quiz.json', 'r') as file:
        fichier_quiz = json.load(file)

    questions = fichier_quiz['questions']
    answers = [question['r'] for question in questions]

    class Quiz:
        def __init__(self, questions, answers):
            self.questions = questions
            self.answers = answers
            self.current_question_index = 0
            self.score = 0

        def get_current_question(self):
            """Retourne la question actuelle sous forme de dictionnaire."""
            return self.questions[self.current_question_index]

        def check_answer(self, selected_option):
            correct_answer = self.get_current_question()['r']
            if selected_option == correct_answer:
                self.score += 1
            self.current_question_index += 1
            return self.current_question_index < len(self.questions)

        def get_score(self):
            """Retourne le score actuel."""
            return self.score

        def get_total_questions(self):
            """Retourne le nombre total de questions."""
            return len(self.questions)

    class QuizApp:
        def __init__(self, root, quiz):
            self.root = root
            self.quiz = quiz

            self.question_label = tk.Label(root, text="", font=("Arial", 16))
            self.question_label.pack(pady=20)

            self.option_buttons = []
            for i in range(3):
                button = tk.Button(root, text="", font=("Arial", 14), width=20, command=lambda i=i: self.check_answer(self.option_buttons[i].cget("text")))
                button.pack(pady=5)
                self.option_buttons.append(button)

            self.next_button = tk.Button(root, text="Suivant", font=("Arial", 14), state=tk.DISABLED, command=self.next_question)
            self.next_button.pack(side=tk.LEFT, padx=10, pady=20)

            self.quit_button = tk.Button(root, text="Quitter", font=("Arial", 14), command=self.quit_quiz)
            self.quit_button.pack(side=tk.RIGHT, padx=10, pady=20)
            self.show_question()

        def show_question(self):
            """Affiche la question actuelle et les options de réponse."""
            question = self.quiz.get_current_question()
            if isinstance(question, dict):
                self.display_question_text(question['q'])
                self.display_options(question)
            else:
                messagebox.showerror("Erreur", "Les données de la question ne sont pas au format attendu.")
                self.root.destroy()

        def display_question_text(self, question_text):
            """Affiche le texte de la question."""
            self.question_label.config(text=question_text)

        def display_options(self, question):
            """Affiche les options de réponse pour la question actuelle."""
            options = [question["r1"], question["r2"], question["r3"]]
            for i, option in enumerate(options):
                self.option_buttons[i].config(text=option, state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)

        def check_answer(self, selected_option):
            """Vérifie la réponse sélectionnée et met à jour l'état des boutons."""
            has_more_questions = self.quiz.check_answer(selected_option)
            self.next_button.config(state=tk.NORMAL if has_more_questions else tk.DISABLED)
            for button in self.option_buttons:
                button.config(state=tk.DISABLED)

            if not has_more_questions:
                self.quit_button.config(state=tk.NORMAL)

        def next_question(self):
            """Affiche la question suivante ou termine le quiz si aucune question restante."""
            if self.quiz.current_question_index < len(self.quiz.questions):
                self.show_question()
            else:
                self.quit_quiz()

        def quit_quiz(self):
            """Affiche le score final et termine le quiz."""
            score = self.quiz.get_score()
            total_questions = self.quiz.get_total_questions()
            messagebox.showinfo("Résultat", f"Score: {score}/{total_questions}")
            self.root.destroy()

    root = tk.Tk()
    root.title("Quiz App")

    quiz = Quiz(questions, answers)

    app = QuizApp(root, quiz)

    root.mainloop()

    cleanup()

run_quiz_app()
