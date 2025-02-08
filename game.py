import tkinter as tk
from tkinter import messagebox
import random

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.wins = 0

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("400x550")
window.configure(bg="#f0f0f0")

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
    return all(buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

def update_status():
    if current_player:
        status_label.config(text=f"Ходит: {current_player.name} ({current_player.symbol})", fg="#333")
    else:
        status_label.config(text="Нажмите 'Начать игру'", fg="#555")
    score_label.config(text=f"🏆 {players[0].name}: {players[0].wins} | {players[1].name}: {players[1].wins}")

def on_click(row, col):
    global current_player
    if current_player is None:
        messagebox.showwarning("Ошибка", "Сначала нажмите 'Начать игру'!")
        return
    if buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player.symbol
    buttons[row][col]['fg'] = "#d9534f" if current_player.symbol == "X" else "#5bc0de"

    if check_winner():
        current_player.wins += 1
        update_status()
        if current_player.wins == 3:
            messagebox.showinfo("Игра окончена", f"🎉 {current_player.name} выиграл матч (3 победы)!")
            restart_game()
        else:
            messagebox.showinfo("Раунд окончен", f"{current_player.name} победил в этом раунде!")
            reset_game()
        return

    if check_draw():
        messagebox.showinfo("Игра окончена", "🤝 Ничья!")
        reset_game()
        return

    current_player = players[1] if current_player == players[0] else players[0]
    update_status()

def reset_game():
    global current_player
    if not players:
        return
    current_player = random.choice(players)
    for i in range(3):
        for j in range(3):
            buttons[i][j]["text"] = ""
    update_status()

def restart_game():
    global players, current_player
    for player in players:
        player.wins = 0
    reset_game()
    frame_inputs.pack(pady=5)  # Показываем ввод имен
    frame_board.pack_forget()  # Скрываем поле

def start_game():
    global players, current_player
    name1 = player1_entry.get().strip()
    name2 = player2_entry.get().strip()

    if not name1 or not name2:
        messagebox.showwarning("Ошибка", "Введите имена обоих игроков!")
        return

    if random_var.get():  # Если чекбокс "Случайный выбор" включен
        symbols = ["X", "O"]
        random.shuffle(symbols)
    else:  # Иначе игроки выбирают сами
        symbol1 = symbol_var1.get()
        symbol2 = "O" if symbol1 == "X" else "X"
        symbols = [symbol1, symbol2]

    players.clear()
    players.append(Player(name1, symbols[0]))
    players.append(Player(name2, symbols[1]))
    current_player = players[0]

    update_status()

    frame_inputs.pack_forget()  # Скрываем ввод имен
    frame_board.pack(pady=10)   # Показываем игровое поле

# Заголовок
title_label = tk.Label(window, text="Крестики-нолики", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

# Поля для ввода имен
frame_inputs = tk.Frame(window, bg="#f0f0f0")
frame_inputs.pack(pady=5)

tk.Label(frame_inputs, text="Имя игрока 1:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
player1_entry = tk.Entry(frame_inputs)
player1_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Имя игрока 2:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="w")
player2_entry = tk.Entry(frame_inputs)
player2_entry.grid(row=1, column=1, padx=5, pady=5)

# Выбор символов
tk.Label(frame_inputs, text="Игрок 1 играет за:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="w")
symbol_var1 = tk.StringVar(value="X")
symbol_x = tk.Radiobutton(frame_inputs, text="X", variable=symbol_var1, value="X", bg="#f0f0f0")
symbol_x.grid(row=2, column=1, sticky="w")
symbol_o = tk.Radiobutton(frame_inputs, text="O", variable=symbol_var1, value="O", bg="#f0f0f0")
symbol_o.grid(row=2, column=2, sticky="w")

# Чекбокс случайного выбора
random_var = tk.BooleanVar()
random_checkbox = tk.Checkbutton(frame_inputs, text="Случайный выбор", variable=random_var, bg="#f0f0f0")
random_checkbox.grid(row=3, column=0, columnspan=2, pady=5)

start_button = tk.Button(window, text="Начать игру", font=("Arial", 12), bg="#5cb85c", fg="white", command=start_game)
start_button.pack(pady=10)

status_label = tk.Label(window, text="Нажмите 'Начать игру'", font=("Arial", 12), bg="#f0f0f0", fg="#555")
status_label.pack(pady=5)

score_label = tk.Label(window, text="", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333")
score_label.pack(pady=5)

# Игровое поле (по умолчанию скрыто)
frame_board = tk.Frame(window, bg="#f0f0f0")
frame_board.pack_forget()

for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(frame_board, text="", font=("Arial", 20, "bold"), width=5, height=2,
                        bg="#ffffff", fg="#333", activebackground="#ddd",
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

frame_buttons = tk.Frame(window, bg="#f0f0f0")
frame_buttons.pack(pady=10)

reset_button = tk.Button(frame_buttons, text="Сброс раунда", font=("Arial", 12), bg="#f0ad4e", fg="white", command=reset_game)
reset_button.pack(side="left", padx=5)

restart_button = tk.Button(frame_buttons, text="Новая игра", font=("Arial", 12), bg="#d9534f", fg="white", command=restart_game)
restart_button.pack(side="right", padx=5)

window.mainloop()
