import tkinter as tk
from tkinter import messagebox
from collections import deque
from heapq import heappop, heappush  # For priority queue in UCS

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe: Play Against AI or Another Player")

        # Initialize game variables
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        self.current_player = 'X'
        self.game_mode = None  # "AI" or "2P"
        self.ai_algorithm = None  # Selected AI algorithm

        # Colors
        self.bg_color = "#2C3E50"
        self.player_color = "#1ABC9C"
        self.ai_color = "#E74C3C"
        self.empty_color = "#95A5A6"

        # Create selection screen
        self.create_selection_screen()
        self.window.mainloop()

    def create_selection_screen(self):
        """Create a screen to choose the game mode and AI algorithm."""
        self.window.config(bg=self.bg_color)
        label = tk.Label(
            self.window, text="Welcome to Tic-Tac-Toe!", font=("Arial", 20, "bold"), bg=self.bg_color, fg="white"
        )
        label.pack(pady=20)

        mode_label = tk.Label(self.window, text="Choose Game Mode", font=("Arial", 16), bg=self.bg_color, fg="white")
        mode_label.pack(pady=10)

        ai_button = tk.Button(
            self.window, text="Play Against Computer", font=("Arial", 14), command=self.choose_ai_algorithm, bg=self.ai_color, fg="white"
        )
        ai_button.pack(pady=10)

        player_button = tk.Button(
            self.window, text="2 Players", font=("Arial", 14), command=lambda: self.start_game("2P"), bg=self.player_color, fg="white"
        )
        player_button.pack(pady=10)

    def choose_ai_algorithm(self):
        """Create a screen to choose the AI algorithm."""
        for widget in self.window.winfo_children():
            widget.destroy()

        label = tk.Label(
            self.window, text="Choose AI Algorithm", font=("Arial", 16), bg=self.bg_color, fg="white"
        )
        label.pack(pady=20)

        bfs_button = tk.Button(
            self.window, text="BFS", font=("Arial", 14), command=lambda: self.start_game("AI", "BFS"), bg=self.ai_color, fg="white"
        )
        bfs_button.pack(pady=10)

        dfs_button = tk.Button(
            self.window, text="DFS", font=("Arial", 14), command=lambda: self.start_game("AI", "DFS"), bg=self.ai_color, fg="white"
        )
        dfs_button.pack(pady=10)

        ucs_button = tk.Button(
            self.window, text="UCS", font=("Arial", 14), command=lambda: self.start_game("AI", "UCS"), bg=self.ai_color, fg="white"
        )
        ucs_button.pack(pady=10)

    def start_game(self, mode, algorithm=None):
        """Start the game in the chosen mode."""
        self.game_mode = mode
        self.ai_algorithm = algorithm
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_board()

    def create_board(self):
        """Create the 3x3 grid for the game."""
        self.window.config(bg=self.bg_color)
        for i in range(9):
            button = tk.Button(
                self.window,
                text=' ',
                font=('Arial', 24, 'bold'),
                height=2,
                width=5,
                bg=self.empty_color,
                fg="white",
                command=lambda i=i: self.player_move(i)
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

    def player_move(self, index):
        """Handle the player's move."""
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.update_button(index)
            if self.check_winner(self.current_player):
                self.end_game(f"{self.current_player} wins!")
            elif self.is_draw():
                self.end_game("It's a draw!")
            else:
                if self.game_mode == "AI" and self.current_player == 'X':
                    self.current_player = 'O'
                    self.window.after(500, self.computer_move)
                elif self.game_mode == "2P":
                    self.current_player = 'O' if self.current_player == 'X' else 'X'

    def computer_move(self):
        """Handle the computer's move."""
        if self.ai_algorithm == "BFS":
            move = self.bfs()
        elif self.ai_algorithm == "DFS":
            move = self.dfs()
        elif self.ai_algorithm == "UCS":
            move = self.ucs()
        else:
            raise ValueError("Invalid AI algorithm selected.")

        self.board[move] = 'O'
        self.update_button(move)
        if self.check_winner('O'):
            self.end_game("AI wins! Better luck next time!")
        elif self.is_draw():
            self.end_game("It's a draw!")
        else:
            self.current_player = 'X'

    def update_button(self, index):
        """Update the button display based on the board."""
        color = self.player_color if self.board[index] == 'X' else self.ai_color
        self.buttons[index].config(text=self.board[index], state=tk.DISABLED, bg=color)

    def bfs(self):
        """AI move using Breadth-First Search."""
        queue = deque([(self.board, None)])
        visited = set()  # Avoid redundant expansions
        while queue:
            state, move = queue.popleft()
            state_tuple = tuple(state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            for i in range(9):
                if state[i] == ' ':
                    new_state = state[:]
                    new_state[i] = 'O'
                    if self.check_winner_simulated(new_state, 'O'):
                        return i
                    queue.append((new_state, i))
        return self.find_first_empty()

    def dfs(self):
        """AI move using Depth-First Search."""
        stack = [(self.board, None)]
        visited = set()  # Avoid redundant expansions
        while stack:
            state, move = stack.pop()
            state_tuple = tuple(state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            for i in range(9):
                if state[i] == ' ':
                    new_state = state[:]
                    new_state[i] = 'O'
                    if self.check_winner_simulated(new_state, 'O'):
                        return i
                    stack.append((new_state, i))
        return self.find_first_empty()

    def ucs(self):
        """AI move using Uniform Cost Search with varying costs."""
        # Define varying costs for each cell
        cell_costs = [9, 10, 4, 1, 2, 13, 4, 2, 6]
        if all(cost == 1 for cost in cell_costs):
            return self.bfs()
        else:
            priority_queue = []  # (cumulative_cost, board_state, move)
        heappush(priority_queue, (0, self.board, None))
        visited = set()  # Avoid redundant expansions

        while priority_queue:
            cost, state, move = heappop(priority_queue)
            state_tuple = tuple(state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            for i in range(9):
                if state[i] == ' ':
                    new_state = state[:]
                    new_state[i] = 'O'
                    new_cost = cost + cell_costs[i]
                    if self.check_winner_simulated(new_state, 'O'):
                        return i
                    heappush(priority_queue, (new_cost, new_state, i))

        return self.find_first_empty()  # Fallback if no winning move is found

    def check_winner_simulated(self, board, player):
        """Simulate and check if a player has won."""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        return any(all(board[pos] == player for pos in condition) for condition in win_conditions)

    def find_first_empty(self):
        """Find the first empty position."""
        for i in range(9):
            if self.board[i] == ' ':
                return i

    def check_winner(self, player):
        """Check if the specified player has won."""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        return any(all(self.board[pos] == player for pos in condition) for condition in win_conditions)

    def is_draw(self):
        """Check if the game is a draw."""
        return ' ' not in self.board

    def end_game(self, result):
        """Create a custom end game pop-up with modern design."""
        end_game_window = tk.Toplevel(self.window)
        end_game_window.title("Game Over")
        end_game_window.geometry("300x200")
        end_game_window.config(bg="#1ABC9C")

        result_label = tk.Label(
            end_game_window, text=result, font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white"
        )
        result_label.pack(pady=30)

        play_again_button = tk.Button(
            end_game_window, text="Play Again", font=("Arial", 14), bg="#E74C3C", fg="white",
            command=lambda: self.reset_game(end_game_window)
        )
        play_again_button.pack(side="left", padx=20, pady=10)

        exit_button = tk.Button(
            end_game_window, text="Exit", font=("Arial", 14), bg="#E74C3C", fg="white",
            command=self.window.quit
        )
        exit_button.pack(side="right", padx=20, pady=10)

        end_game_window.eval('tk::PlaceWindow %s center' % end_game_window.winfo_toplevel())

    def reset_game(self, end_game_window):
        """Reset the game state and go back to the mode selection screen."""
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        self.current_player = 'X'
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_selection_screen()

if __name__ == "__main__":
    TicTacToe()
