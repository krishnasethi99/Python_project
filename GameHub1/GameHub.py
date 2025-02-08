import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy

class GameHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Hub")
        self.root.geometry("400x300")
        self.dark_mode = False
        
        self.scoreboard = {"Minesweeper": 0, "Tic-Tac-Toe": 0, "Sudoku": 0}
        
        self.create_menu()
        self.create_widgets()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Game Rules", command=self.show_rules)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Menu", menu=game_menu)
        
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)
        menubar.add_cascade(label="Theme", menu=theme_menu)
    
    def create_widgets(self):
        tk.Label(self.root, text="Choose a Game", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.root, text="Minesweeper", command=self.open_minesweeper).pack(pady=5)
        tk.Button(self.root, text="Tic-Tac-Toe", command=self.open_tictactoe).pack(pady=5)
        tk.Button(self.root, text="Sudoku", command=self.open_sudoku).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#333" if self.dark_mode else "#FFF"
        fg_color = "#FFF" if self.dark_mode else "#000"
        self.root.configure(bg=bg_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.configure(bg=bg_color, fg=fg_color)
    
    def show_rules(self):
        rules = """
        1. Minesweeper - Avoid clicking on mines. Right-click to flag.
        2. Tic-Tac-Toe - Get three in a row to win. Play against AI or a friend.
        3. Sudoku - Fill the grid so each row, column, and 3x3 section contains 1-9.
        """
        messagebox.showinfo("Game Rules", rules)
    
    def update_score(self, game):
        self.scoreboard[game] += 1
        messagebox.showinfo("Score Update", f"{game} Score: {self.scoreboard[game]}")
    
    def open_minesweeper(self):
        Minesweeper(self.root)
    
    def open_tictactoe(self):
        TicTacToe(self.root)
    
    def open_sudoku(self):
        Sudoku(self.root)

class Minesweeper:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Minesweeper")
        self.difficulty_levels = {"Easy": (5, 5, 5), "Medium": (8, 8, 12), "Hard": (12, 12, 20)}
        
        self.create_menu()
        self.set_difficulty("Medium")
    
    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        difficulty_menu = tk.Menu(menubar, tearoff=0)
        for level in self.difficulty_levels.keys():
            difficulty_menu.add_command(label=level, command=lambda l=level: self.set_difficulty(l))
        menubar.add_cascade(label="Difficulty", menu=difficulty_menu)
    
    def set_difficulty(self, level):
        self.rows, self.cols, self.mines = self.difficulty_levels[level]
        self.setup_board()
    
    def setup_board(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = set()
        self.revealed = set()
        self.place_mines()
        self.calculate_hints()
        
        self.buttons = {}
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.master, width=4, height=2, font=("Arial", 12, "bold"), relief=tk.RAISED, bg="lightgray", command=lambda row=r, col=c: self.reveal_cell(row, col))
                btn.grid(row=r, column=c, padx=2, pady=2)
                btn.bind("<Button-3>", lambda event, row=r, col=c: self.flag_cell(row, col))
                self.buttons[(r, c)] = btn
    
    def place_mines(self):
        mine_positions = random.sample(range(self.rows * self.cols), self.mines)
        for pos in mine_positions:
            r, c = divmod(pos, self.cols)
            self.board[r][c] = -1
    
    def calculate_hints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1] 
                            if 0 <= r+dr < self.rows and 0 <= c+dc < self.cols 
                            and self.board[r+dr][c+dc] == -1)
                self.board[r][c] = count
    
    def reveal_cell(self, row, col):
        if (row, col) in self.flags or (row, col) in self.revealed:
            return
        
        if self.board[row][col] == -1:
            messagebox.showerror("Game Over", "You hit a mine!")
            self.setup_board()
            return
        
        self.revealed.add((row, col))
        btn = self.buttons[(row, col)]
        btn.config(text="✅", state="disabled", bg="white")
    
    def flag_cell(self, row, col):
        if (row, col) in self.flags:
            self.flags.remove((row, col))
            self.buttons[(row, col)].config(text="", bg="lightgray")
        else:
            self.flags.add((row, col))
            self.buttons[(row, col)].config(text="🚩", bg="yellow")
            
class TicTacToe:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Tic-Tac-Toe")
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.create_board()
    
    def create_board(self):
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.master, text="", font=("Arial", 24), width=5, height=2,
                                command=lambda row=r, col=c: self.make_move(row, col))
                btn.grid(row=r, column=c)
                self.board[r][c] = btn
    
    def make_move(self, row, col):
        if self.board[row][col]["text"] == "":
            self.board[row][col]["text"] = self.current_player
            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"{self.current_player} Wins!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.ai_move()
    
    def check_winner(self, player):
        for row in self.board:
            if all(btn["text"] == player for btn in row):
                return True
        for col in range(3):
            if all(self.board[row][col]["text"] == player for row in range(3)):
                return True
        if all(self.board[i][i]["text"] == player for i in range(3)) or all(self.board[i][2-i]["text"] == player for i in range(3)):
            return True
        return False
    
    def ai_move(self):
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c]["text"] == ""]
        if available_moves:
            row, col = random.choice(available_moves)
            self.make_move(row, col)
    
    def reset_board(self):
        for row in self.board:
            for btn in row:
                btn["text"] = ""
        self.current_player = "X"
        
class Sudoku:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Sudoku")
        self.difficulty_levels = {"Easy": 40, "Medium": 30, "Hard": 20}
        self.create_menu()
        self.set_difficulty("Medium")
    
    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        difficulty_menu = tk.Menu(menubar, tearoff=0)
        for level in self.difficulty_levels.keys():
            difficulty_menu.add_command(label=level, command=lambda l=level: self.set_difficulty(l))
        menubar.add_cascade(label="Difficulty", menu=difficulty_menu)
        
        hint_menu = tk.Menu(menubar, tearoff=0)
        hint_menu.add_command(label="Get Hint", command=self.get_hint)
        menubar.add_cascade(label="Hints", menu=hint_menu)
    
    def set_difficulty(self, level):
        self.clues = self.difficulty_levels[level]
        self.generate_puzzle()
    
    def generate_puzzle(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_board(self.board)
        self.puzzle = copy.deepcopy(self.board)
        self.remove_numbers()
        self.draw_board()
    
    def solve_board(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty
        for num in random.sample(range(1, 10), 9):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                if self.solve_board(board):
                    return True
                board[row][col] = 0
        return False
    
    def find_empty(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None
    
    def is_valid(self, board, num, pos):
        r, c = pos
        if num in board[r] or num in [board[i][c] for i in range(9)]:
            return False
        box_x, box_y = c // 3, r // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num:
                    return False
        return True
    
    def remove_numbers(self):
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        for _ in range(81 - self.clues):
            r, c = cells.pop()
            self.puzzle[r][c] = 0
    
    def draw_board(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.entries = {}
        for r in range(9):
            for c in range(9):
                val = self.puzzle[r][c]
                entry = tk.Entry(self.master, width=3, font=("Arial", 18), justify="center", relief=tk.RIDGE, bd=2)
                entry.grid(row=r, column=c, padx=(2 if c % 3 == 0 else 0), pady=(2 if r % 3 == 0 else 0))
                if val:
                    entry.insert(0, str(val))
                    entry.config(state="disabled")
                self.entries[(r, c)] = entry
    
    def get_hint(self):
        empty = [(r, c) for r in range(9) for c in range(9) if self.entries[(r, c)].get() == ""]
        if empty:
            r, c = random.choice(empty)
            self.entries[(r, c)].insert(0, str(self.board[r][c]))
            self.entries[(r, c)].config(state="disabled")
            

if __name__ == "__main__":
    root = tk.Tk()
    app = GameHub(root)
    root.mainloop()