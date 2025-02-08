import tkinter as tk
from tkinter import messagebox
import random

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.wins = 0  # Счетчик побед

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("350x600")

buttons = []
players = []
current_player = None

def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return True

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return True

    return False

def check_draw():
    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == "":
                return False
    return True

def update_status():
    if current_player:
        status_label.config(text=f"Ходит: {current_player.name} ({current_player.symbol})")
    else:
        status_label.config(text="Нажмите 'Начать игру'")

    # Обновляем счетчик побед
    score_label.config(text=f"{players[0].name}: {players[0].wins} | {players[1].name}: {players[1].wins}")

def on_click(row, col):
    global current_player

    if current_player is None:
        messagebox.showwarning("Ошибка", "Сначала нажмите 'Начать игру'!")
        return

    if buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player.symbol

    if check_winner():
        current_player.wins += 1  # Увеличиваем счетчик побед
        update_status()

        if current_player.wins == 3:
            messagebox.showinfo("Игра окончена", f"{current_player.name} ({current_player.symbol}) одержал 3 победы и выиграл матч!")
            restart_game()
        else:
            messagebox.showinfo("Раунд окончен", f"{current_player.name} ({current_player.symbol}) победил в этом раунде!")
            reset_game()
        return

    if check_draw():
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_game()
        return

    current_player = players[1] if current_player == players[0] else players[0]
    update_status()

def reset_game():
    """Сбрасывает поле, но оставляет счетчик побед."""
    global current_player
    if not players:
        return
    current_player = random.choice(players)
    for i in range(3):
        for j in range(3):
            buttons[i][j]["text"] = ""
    update_status()

def restart_game():
    """Полностью сбрасывает игру, включая счетчики побед."""
    global players, current_player
    for player in players:
        player.wins = 0
    reset_game()

def start_game():
    global players, current_player
    name1 = player1_entry.get().strip()
    name2 = player2_entry.get().strip()

    if not name1 or not name2:
        messagebox.showwarning("Ошибка", "Введите имена обоих игроков!")
        return

    symbols = ["X", "O"]
    random.shuffle(symbols)
    players.clear()
    players.append(Player(name1, symbols[0]))
    players.append(Player(name2, symbols[1]))
    current_player = players[0]

    update_status()

# Поля для ввода имен
tk.Label(window, text="Имя игрока 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
player1_entry = tk.Entry(window)
player1_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(window, text="Имя игрока 2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
player2_entry = tk.Entry(window)
player2_entry.grid(row=1, column=1, padx=5, pady=5)

start_button = tk.Button(window, text="Начать игру", command=start_game)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

status_label = tk.Label(window, text="Нажмите 'Начать игру'", font=("Arial", 12))
status_label.grid(row=3, column=0, columnspan=2, pady=5)

score_label = tk.Label(window, text="", font=("Arial", 12))  # Поле для счета
score_label.grid(row=4, column=0, columnspan=2, pady=5)

# Создание игрового поля
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2, command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i+5, column=j, padx=10, pady=5)
        row.append(btn)
    buttons.append(row)

reset_button = tk.Button(window, text="Сброс раунда", font=("Arial", 14), command=reset_game)
reset_button.grid(row=9, column=0, columnspan=3, pady=10)

restart_button = tk.Button(window, text="Новая игра", font=("Arial", 14), command=restart_game)
restart_button.grid(row=10, column=0, columnspan=3, pady=5)

window.mainloop()
