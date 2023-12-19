import tkinter as tk
import random

class Buscaminas:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Buscaminas")
        self.size = 20
        self.bomb_count = 45
        self.buttons = []
        self.is_game_over = False
        self.flags = [[False for _ in range(self.size)] for _ in range(self.size)]

        self.generate_board()
        self.place_bombs()
        self.calculate_numbers()
        self.create_board()

    # Crea el tablero
    def generate_board(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

    # Colocar bombas en las celdas
    def place_bombs(self):
        bombs_placed = 0
        while bombs_placed < self.bomb_count:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[x][y] != -1:
                self.board[x][y] = -1
                bombs_placed += 1

    # Indica el numero de bombas adyacentes a un celda
    def calculate_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != -1:
                    self.board[i][j] = self.count_adjacent_bombs(i, j)

    # Cuenta las minas adyacentes a las celdas
    def count_adjacent_bombs(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (
                    0 <= x + i < self.size
                    and 0 <= y + j < self.size
                    and self.board[x + i][y + j] == -1
                ):
                    count += 1
        return count

    # Crea las celdas
    def create_board(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(
                    self.root, width=2, command=lambda x=i, y=j: self.click(x, y)
                )
                button.bind("<Button-3>", lambda event, x=i, y=j: self.place_flag(x, y))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    # Maneja cuando se apreta una celda con bomba
    def click(self, x, y):
        if self.is_game_over or self.flags[x][y]:
            return

        if self.board[x][y] == -1:
            self.reveal_board()
            self.game_over()
        else:
            self.reveal_cell(x, y)
            if self.check_win():
                self.game_won()

    # Metodo que revela celdas adyacentes vacias
    def reveal_cell(self, x, y):
        if self.board[x][y] == 0:
            self.buttons[x][y].config(text="", state=tk.DISABLED, bg="lightgray")
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (
                        0 <= x + i < self.size
                        and 0 <= y + j < self.size
                        and self.buttons[x + i][y + j]["state"] != tk.DISABLED
                    ):
                        self.reveal_cell(x + i, y + j)
        else:
            self.buttons[x][y].config(
                text=self.board[x][y], state=tk.DISABLED, bg="lightgray"
            )

    # Muesta las bombas al finalizar el juego
    def reveal_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -1:
                    self.buttons[i][j].config(text="B")
                    self.buttons[i][j].config(
                        fg="red"
                    )
                else:
                    self.buttons[i][j].config(text=self.board[i][j], state=tk.DISABLED)

    # Detecta cuando se gana el juego. (Cantidad de celdas descubiertas == cantidad de celdas - cantidad de minas)
    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if (
                    self.board[i][j] != -1
                    and self.buttons[i][j]["state"] != tk.DISABLED
                ):
                    return False
        return True

    # Indica cuando se pierde el juego
    def game_over(self):
        self.is_game_over = True
        game_over_label = tk.Label(self.root, text="Game Over!", fg="red")
        game_over_label.grid(row=self.size + 1, columnspan=self.size)
        self.show_retry_menu()

    # Indica cuando se gana el juego
    def game_won(self):
        self.is_game_over = True
        game_won_label = tk.Label(self.root, text="You Won!", fg="green")
        game_won_label.grid(row=self.size + 1, columnspan=self.size)
        self.show_retry_menu()

    # Menu al perder o ganar
    def show_retry_menu(self):
        retry_menu = tk.Menu(self.root, tearoff=0)
        retry_menu.add_command(label="Retry", command=self.start_new_game)
        retry_menu.add_separator()
        retry_menu.add_command(label="Yes", command=self.start_new_game)
        retry_menu.add_command(label="No", command=self.quit_game)

        self.root.config(menu=retry_menu)

    # Reinicia la partida
    def start_new_game(self):
        self.root.destroy()
        self.__init__()
        self.start()

    # Cierra la ventana del juego
    def quit_game(self):
        self.root.destroy()

    # Permite poner las 'Banderas'. Solo si es una celda vacia
    def place_flag(self, x, y):
        if not self.is_game_over and self.buttons[x][y]["state"] != tk.DISABLED:
            if self.flags[x][y]:
                self.buttons[x][y].config(text="", fg="black")
            else:
                if not self.flags[x][y]:
                    self.buttons[x][y].config(text="F", fg="blue")
            self.flags[x][y] = not self.flags[x][y]

    # Comienza una partida
    def start(self):
        self.root.mainloop()


buscaminas = Buscaminas()
buscaminas.start()
