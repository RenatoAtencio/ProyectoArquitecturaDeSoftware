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
        self.size = 15
        self.bomb_count = 45
        self.buttons = []
        self.is_game_over = False
        self.flags = [[False for _ in range(self.size)] for _ in range(self.size)]

        self.generate_board()
        self.place_bombs()
        self.calculate_numbers()
        self.create_board()
   
    # Este método inicializa la matriz que representa el tablero del juego con celdas vacías 
    #(inicialmente todas las celdas tienen el valor 0).
    def generate_board(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
 
    # Coloca las minas en posiciones aleatorias en el tablero. Se asegura de que las minas no se superpongan en la misma celda.
    def place_bombs(self):
        bombs_placed = 0
        while bombs_placed < self.bomb_count:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[x][y] != -1:
                self.board[x][y] = -1
                bombs_placed += 1
  
    # Calcula el número de minas adyacentes a cada celda que no contenga una mina. 
    # Para cada celda vacía, cuenta la cantidad de minas en su vecindad y actualiza ese número en la matriz del tablero.
    def calculate_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != -1:
                    self.board[i][j] = self.count_adjacent_bombs(i, j)
    
   
    # Cuenta el número de minas adyacentes a una celda dada en el tablero.
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

    #: Crea los botones en la interfaz gráfica. Configura los botones y los vincula con métodos específicos 
    # (click y place_flag) cuando se hace clic o se hace clic derecho (para colocar una bandera).
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

    # Maneja el evento cuando se hace clic en una celda del tablero. Si la celda contiene una mina, revela todo el tablero y muestra 
    # "Game Over". De lo contrario, revela la celda y verifica si se ha ganado el juego.
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

    #Método recursivo que revela una celda y, si esa celda está vacía, revela recursivamente las celdas adyacentes vacías.
    def reveal_cell(self, x, y):
        if self.board[x][y] == 0:
            self.buttons[x][y].config(text="", state=tk.DISABLED)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (
                        0 <= x + i < self.size
                        and 0 <= y + j < self.size
                        and self.buttons[x + i][y + j]["state"] != tk.DISABLED
                    ):
                        self.reveal_cell(x + i, y + j)
        else:
            self.buttons[x][y].config(text=self.board[x][y], state=tk.DISABLED)

    #Revela todas las celdas del tablero al finalizar el juego, mostrando las minas y los números.
    def reveal_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -1:
                    self.buttons[i][j].config(text="B")
                    self.buttons[i][j].config(
                        fg="red"
                    )  # Establecer el color rojo después de configurar el texto como 'B'
                else:
                    self.buttons[i][j].config(text=self.board[i][j], state=tk.DISABLED)

    # Verifica si se han revelado todas las celdas que no contienen minas, lo que indicaría que el juego ha sido ganado.
    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if (
                    self.board[i][j] != -1
                    and self.buttons[i][j]["state"] != tk.DISABLED
                ):
                    return False
        return True

    #Maneja el final del juego mostrando "Game Over" en la interfaz y muestra un menú para reiniciar o salir.
    def game_over(self):
        self.is_game_over = True
        game_over_label = tk.Label(self.root, text="Game Over!", fg="red")
        game_over_label.grid(row=self.size + 1, columnspan=self.size)
        self.show_retry_menu()

    # Crea un menú desplegable con opciones para reintentar el juego o salir.
    def show_retry_menu(self):
        retry_menu = tk.Menu(self.root, tearoff=0)
        retry_menu.add_command(label="Retry", command=self.start_new_game)
        retry_menu.add_separator()
        retry_menu.add_command(label="Yes", command=self.start_new_game)
        retry_menu.add_command(label="No", command=self.quit_game)

        self.root.config(menu=retry_menu)

    # Reinicia el juego destruyendo la ventana actual y creando una nueva instancia del juego.
    def start_new_game(self):
        self.root.destroy()
        self.__init__()
        self.start()

    #Cierra la ventana del juego
    def quit_game(self):
        self.root.destroy()

    # Maneja la condición de victoria, mostrando "You Won!" en la interfaz y ofreciendo opciones para reiniciar o salir.
    def game_won(self):
        self.is_game_over = True
        game_won_label = tk.Label(self.root, text="You Won!", fg="green")
        game_won_label.grid(row=self.size + 1, columnspan=self.size)
        self.show_retry_menu()

    #Coloca o quita una bandera en una celda, indicando la posible ubicación de una mina.
    def place_flag(self, x, y):
        if not self.is_game_over:
            if self.flags[x][y]:
                self.buttons[x][y].config(text="", fg="black")
            else:
                self.buttons[x][y].config(text="F", fg="blue")
            self.flags[x][y] = not self.flags[x][y]

    def start(self):
        self.root.mainloop()


buscaminas = Buscaminas()
buscaminas.start()
