"""Colección de minijuegos con interfaz Tkinter.

Incluye Piedra, Papel, Tijera, "Adivina el número", Tic Tac Toe,
Ahorcado y un Quiz Matemático. La estética se mejora usando widgets ttk.
"""

import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


MOVES_NORMAL = {
    'pi': 'Piedra',
    'pa': 'Papel',
    'ti': 'Tijera'
}

MOVES_LOCO = {
    'pi': 'Piedra',
    'pa': 'Papel',
    'ti': 'Tijera',
    'la': 'Lagarto',
    'sp': 'Spock'
}

WIN_CONDITIONS = {
    'pi': ['ti', 'la'],
    'pa': ['pi', 'sp'],
    'ti': ['pa', 'la'],
    'la': ['sp', 'pa'],
    'sp': ['ti', 'pi']
}


class MainApp:
    """Pantalla principal de selección de juegos."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Minijuegos")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#e0e0e0')
        self.style.configure('TButton', padding=6)
        self.root.configure(background='#e0e0e0')
        self.show_menu()

    def clear(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_menu(self) -> None:
        self.clear()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, text="Selecciona un juego", font=("Arial", 14)).grid(
            row=0, column=0, columnspan=3, pady=10
        )
        ttk.Button(frame, text="Piedra, Papel, Tijera", command=self.start_rps).grid(
            row=1, column=0, padx=5, pady=5
        )
        ttk.Button(frame, text="Adivina el número", command=self.start_guess).grid(
            row=1, column=1, padx=5, pady=5
        )
        ttk.Button(frame, text="Tic Tac Toe", command=self.start_ttt).grid(
            row=1, column=2, padx=5, pady=5
        )
        ttk.Button(frame, text="Ahorcado", command=self.start_hangman).grid(
            row=2, column=0, padx=5, pady=5
        )
        ttk.Button(frame, text="Quiz Matemático", command=self.start_math).grid(
            row=2, column=1, padx=5, pady=5
        )

    def start_rps(self) -> None:
        self.clear()
        RPSGame(self.root, self.show_menu)

    def start_guess(self) -> None:
        self.clear()
        GuessNumberGame(self.root, self.show_menu)

    def start_ttt(self) -> None:
        self.clear()
        TicTacToeGame(self.root, self.show_menu)

    def start_hangman(self) -> None:
        self.clear()
        HangmanGame(self.root, self.show_menu)

    def start_math(self) -> None:
        self.clear()
        MathQuizGame(self.root, self.show_menu)


class RPSGame:
    """Juego de Piedra, Papel, Tijera."""

    def __init__(self, root: tk.Tk, back_callback) -> None:
        self.root = root
        self.back_callback = back_callback
        self.players_var = tk.IntVar(value=1)
        self.difficulty_var = tk.StringVar(value='facil')
        self.loco_var = tk.BooleanVar(value=False)
        self.player_turn = 1
        self.choices = {}
        self.scores = {1: 0, 2: 0}
        self.build_config()

    def build_config(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, text='Jugadores').grid(row=0, column=0, sticky="w")
        ttk.OptionMenu(frame, self.players_var, 1, 1, 2).grid(row=0, column=1)

        ttk.Label(frame, text='Dificultad').grid(row=1, column=0, sticky="w")
        ttk.OptionMenu(frame, self.difficulty_var, 'facil', 'facil', 'dificil').grid(
            row=1, column=1
        )

        ttk.Checkbutton(frame, text='Modo loco', variable=self.loco_var).grid(
            row=2, column=0, columnspan=2
        )

        ttk.Button(frame, text='Comenzar', command=self.start_game).grid(
            row=3, column=0, columnspan=2, pady=10
        )
        ttk.Button(frame, text='Volver', command=self.back_callback).grid(
            row=4, column=0, columnspan=2
        )

    def start_game(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()
        self.moves = MOVES_LOCO if self.loco_var.get() else MOVES_NORMAL
        self.create_board()

    def create_board(self) -> None:
        top = ttk.Frame(self.root, padding=10)
        top.pack()
        self.score_label = ttk.Label(
            top, text=f"Marcador: J1 {self.scores[1]} - J2 {self.scores[2]}"
        )
        self.score_label.pack()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        self.buttons = {}
        for key, label in self.moves.items():
            btn = ttk.Button(frame, text=label, width=12, command=lambda k=key: self.choose(k))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.buttons[key] = btn

        bottom = ttk.Frame(self.root, padding=10)
        bottom.pack()
        self.status = ttk.Label(bottom, text='Turno del jugador 1')
        self.status.pack(side=tk.LEFT)
        ttk.Button(bottom, text='Reiniciar', command=self.reset_scores).pack(side=tk.LEFT, padx=10)
        ttk.Button(bottom, text='Volver', command=self.back_callback).pack(side=tk.LEFT)

    def reset_scores(self) -> None:
        self.scores = {1: 0, 2: 0}
        self.update_score()

    def update_score(self) -> None:
        self.score_label.config(
            text=f"Marcador: J1 {self.scores[1]} - J2 {self.scores[2]}"
        )

    def choose(self, move: str) -> None:
        self.choices[f'player{self.player_turn}'] = move
        if self.players_var.get() == 1:
            self.choices['player2'] = self.computer_move(move)
            self.end_round()
        else:
            if self.player_turn == 1:
                self.player_turn = 2
                self.status.config(text='Turno del jugador 2')
            else:
                self.end_round()

    def computer_move(self, user_move: str) -> str:
        if self.difficulty_var.get() == 'facil':
            return random.choice(list(self.moves.keys()))
        for move in self.moves.keys():
            if user_move in WIN_CONDITIONS.get(move, []):
                return move
        return random.choice(list(self.moves.keys()))

    def end_round(self) -> None:
        player1 = self.choices['player1']
        player2 = self.choices['player2']
        if player1 == player2:
            result = 'Empate'
        elif player2 in WIN_CONDITIONS.get(player1, []):
            result = 'Jugador 1 gana'
            self.scores[1] += 1
        elif player1 in WIN_CONDITIONS.get(player2, []):
            result = 'Jugador 2 gana'
            self.scores[2] += 1
        else:
            result = 'Resultado desconocido'
        messagebox.showinfo('Resultado', result)
        self.update_score()
        self.choices = {}
        self.player_turn = 1
        self.status.config(text='Turno del jugador 1')


class GuessNumberGame:
    """Juego sencillo para adivinar un número entre 1 y 10."""

    def __init__(self, root: tk.Tk, back_callback) -> None:
        self.root = root
        self.back_callback = back_callback
        self.secret = random.randint(1, 10)
        self.build_board()

    def build_board(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, text='Adivina un número del 1 al 10').grid(
            row=0, column=0, columnspan=2, pady=5
        )
        self.entry = ttk.Entry(frame, width=5)
        self.entry.grid(row=1, column=0, padx=5)
        ttk.Button(frame, text='Probar', command=self.check).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text='Volver', command=self.back_callback).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def check(self) -> None:
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showerror('Error', 'Introduce un número válido')
            return
        if guess == self.secret:
            messagebox.showinfo('Éxito', '¡Adivinaste!')
            self.secret = random.randint(1, 10)
        elif guess < self.secret:
            messagebox.showinfo('Pista', 'Demasiado bajo')
        else:
            messagebox.showinfo('Pista', 'Demasiado alto')


class TicTacToeGame:
    """Clásico juego del gato con dos dificultades."""

    def __init__(self, root: tk.Tk, back_callback) -> None:
        self.root = root
        self.back_callback = back_callback
        self.difficulty_var = tk.StringVar(value='facil')
        self.build_config()

    def build_config(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, text='Dificultad').grid(row=0, column=0, sticky='w')
        ttk.OptionMenu(frame, self.difficulty_var, 'facil', 'facil', 'dificil').grid(
            row=0, column=1
        )
        ttk.Button(frame, text='Comenzar', command=self.start_game).grid(
            row=1, column=0, columnspan=2, pady=5
        )
        ttk.Button(frame, text='Volver', command=self.back_callback).grid(
            row=2, column=0, columnspan=2
        )

    def start_game(self) -> None:
        for w in self.root.winfo_children():
            w.destroy()
        self.board = [''] * 9
        self.buttons = []
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        for i in range(9):
            btn = ttk.Button(
                frame, text='', width=5, command=lambda i=i: self.player_move(i)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)
        ttk.Button(self.root, text='Volver', command=self.back_callback).pack(pady=10)

    def player_move(self, idx: int) -> None:
        if self.board[idx] or self.check_winner():
            return
        self.board[idx] = 'X'
        self.buttons[idx].config(text='X', state='disabled')
        if self.check_winner():
            messagebox.showinfo('Fin', '¡Ganaste!')
            self.start_game()
            return
        self.computer_move()

    def computer_move(self) -> None:
        empty = [i for i, v in enumerate(self.board) if not v]
        if not empty:
            messagebox.showinfo('Fin', 'Empate')
            self.start_game()
            return
        if self.difficulty_var.get() == 'dificil':
            move = self.find_winning_move('O') or self.find_winning_move('X')
            if move is None:
                move = random.choice(empty)
        else:
            move = random.choice(empty)
        self.board[move] = 'O'
        self.buttons[move].config(text='O', state='disabled')
        if self.check_winner():
            messagebox.showinfo('Fin', 'La computadora ganó')
            self.start_game()
        elif all(self.board):
            messagebox.showinfo('Fin', 'Empate')
            self.start_game()

    def find_winning_move(self, player: str):
        combos = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in combos:
            line = [self.board[a], self.board[b], self.board[c]]
            if line.count(player) == 2 and line.count('') == 1:
                if self.board[a] == '':
                    return a
                if self.board[b] == '':
                    return b
                return c
        return None

    def check_winner(self) -> bool:
        combos = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in combos:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return True
        return False


class HangmanGame:
    """Juego del ahorcado con selección de dificultad."""

    WORDS = [
        'casa', 'perro', 'gato', 'python', 'programa', 'computadora',
        'teclado', 'raton', 'ventana', 'internet'
    ]

    def __init__(self, root: tk.Tk, back_callback) -> None:
        self.root = root
        self.back_callback = back_callback
        self.difficulty_var = tk.StringVar(value='facil')
        self.build_config()

    def build_config(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, text='Dificultad').grid(row=0, column=0, sticky='w')
        ttk.OptionMenu(frame, self.difficulty_var, 'facil', 'facil', 'dificil').grid(
            row=0, column=1
        )
        ttk.Button(frame, text='Comenzar', command=self.start_game).grid(
            row=1, column=0, columnspan=2, pady=5
        )
        ttk.Button(frame, text='Volver', command=self.back_callback).grid(
            row=2, column=0, columnspan=2
        )

    def start_game(self) -> None:
        for w in self.root.winfo_children():
            w.destroy()
        if self.difficulty_var.get() == 'facil':
            pool = [w for w in self.WORDS if len(w) <= 5]
            self.attempts = 8
        else:
            pool = [w for w in self.WORDS if len(w) > 5]
            self.attempts = 6
        self.secret = random.choice(pool)
        self.guessed = set()
        self.display_var = tk.StringVar(value='_ ' * len(self.secret))
        self.info_var = tk.StringVar(value=f'Intentos restantes: {self.attempts}')
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, textvariable=self.display_var, font=('Courier', 16)).grid(
            row=0, column=0, columnspan=2, pady=5
        )
        self.entry = ttk.Entry(frame, width=5)
        self.entry.grid(row=1, column=0, pady=5)
        ttk.Button(frame, text='Probar', command=self.check).grid(
            row=1, column=1, padx=5
        )
        ttk.Label(frame, textvariable=self.info_var).grid(
            row=2, column=0, columnspan=2, pady=5
        )
        ttk.Button(frame, text='Volver', command=self.back_callback).grid(
            row=3, column=0, columnspan=2, pady=5
        )

    def check(self) -> None:
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        if len(letter) != 1 or not letter.isalpha():
            messagebox.showerror('Error', 'Introduce una sola letra')
            return
        if letter in self.guessed:
            return
        self.guessed.add(letter)
        if letter not in self.secret:
            self.attempts -= 1
        display = ' '.join([c if c in self.guessed else '_' for c in self.secret])
        self.display_var.set(display)
        self.info_var.set(f'Intentos restantes: {self.attempts}')
        if all(c in self.guessed for c in self.secret):
            messagebox.showinfo('Fin', '¡Ganaste!')
            self.start_game()
        elif self.attempts <= 0:
            messagebox.showinfo('Fin', f'Perdiste. Era {self.secret}')
            self.start_game()


class MathQuizGame:
    """Juego de preguntas matemáticas con tres dificultades."""

    def __init__(self, root: tk.Tk, back_callback) -> None:
        self.root = root
        self.back_callback = back_callback
        self.difficulty_var = tk.StringVar(value='facil')
        self.score = 0
        self.build_config()

    def build_config(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, text='Dificultad').grid(row=0, column=0, sticky='w')
        ttk.OptionMenu(
            frame, self.difficulty_var, 'facil', 'facil', 'media', 'dificil'
        ).grid(row=0, column=1)
        ttk.Button(frame, text='Comenzar', command=self.start_game).grid(
            row=1, column=0, columnspan=2, pady=5
        )
        ttk.Button(frame, text='Volver', command=self.back_callback).grid(
            row=2, column=0, columnspan=2
        )

    def start_game(self) -> None:
        for w in self.root.winfo_children():
            w.destroy()
        self.score = 0
        self.question_var = tk.StringVar()
        self.score_var = tk.StringVar(value='Puntuación: 0')
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()
        ttk.Label(frame, textvariable=self.question_var, font=('Arial', 14)).grid(
            row=0, column=0, columnspan=2, pady=5
        )
        self.entry = ttk.Entry(frame, width=5)
        self.entry.grid(row=1, column=0, pady=5)
        ttk.Button(frame, text='Responder', command=self.check).grid(
            row=1, column=1, padx=5
        )
        ttk.Label(frame, textvariable=self.score_var).grid(
            row=2, column=0, columnspan=2, pady=5
        )
        ttk.Button(frame, text='Volver', command=self.back_callback).grid(
            row=3, column=0, columnspan=2, pady=5
        )
        self.new_question()

    def new_question(self) -> None:
        d = self.difficulty_var.get()
        if d == 'facil':
            a, b = random.randint(1, 10), random.randint(1, 10)
            self.answer = a + b
            self.question_var.set(f'{a} + {b} = ?')
        elif d == 'media':
            a, b = random.randint(1, 20), random.randint(1, 20)
            if random.choice([True, False]):
                self.answer = a + b
                self.question_var.set(f'{a} + {b} = ?')
            else:
                self.answer = a - b
                self.question_var.set(f'{a} - {b} = ?')
        else:
            a, b = random.randint(1, 12), random.randint(1, 12)
            self.answer = a * b
            self.question_var.set(f'{a} × {b} = ?')

    def check(self) -> None:
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showerror('Error', 'Introduce un número')
            return
        if guess == self.answer:
            self.score += 1
            self.score_var.set(f'Puntuación: {self.score}')
            self.entry.delete(0, tk.END)
            self.new_question()
        else:
            messagebox.showinfo('Fin', f'Incorrecto. Puntuación final: {self.score}')
            self.start_game()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

