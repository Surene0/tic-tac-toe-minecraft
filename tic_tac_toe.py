import tkinter as tk
from tkinter import messagebox
import random

# Размеры и отступы
BLOCK_SIZE = 100
BLOCK_PAD = 6
FONT_PX = ("Minecraft", 24, "bold")

# Цветовая палитра в стиле Minecraft
BG_COLOR = "#3d3d3d"  # Тёмно-серый фон
GRID_BG = "#5c5c5c"  # Серый для сетки
CELL_BG = "#8b6f47"  # Коричневый (дерево)
CELL_EDGE = "#4a3520"  # Тёмный контур
X_COLOR = "#2ecf6e"  # Зелёный (как трава)
O_COLOR = "#3aa3f7"  # Голубой (как вода)
TEXT_COLOR = "#f0f0f0"  # Светлый текст
BUTTON_BG = "#6b4226"  # Кнопка (дерево)
BUTTON_HOVER = "#8c5a32"  # Наведение (тёмное дерево)
RESET_BG = "#4b6e2b"  # Зелёный для сброса (трава)

class PixelStoneTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики‑нолики Майнкрафт")
        self.root.resizable(False, False)
        self.current = "X"
        self.grid = [[None] * 3 for _ in range(3)]
        self.moves = 0
        self.scores = {"X": 0, "O": 0, "Tie": 0}
        self._build_ui()

    def _build_ui(self):
        # Основной фон
        self.root.configure(bg=BG_COLOR)

        # Заголовок с текстурой
        header = tk.Label(
            self.root,
            text="КРЕСТИКИ‑НОЛИКИ",
            font=("Minecraft", 28, "bold"),
            fg="#e7e7e7",
            bg=BG_COLOR,
            padx=20,
            pady=10
        )
        header.grid(row=0, column=0, columnspan=3, pady=(15, 5))

        # Рамка для игрового поля
        frame = tk.Frame(self.root, bg=GRID_BG, bd=4, relief="sunken")
        frame.grid(row=1, column=0, columnspan=3, padx=25, pady=15)

        # Создание клеток с текстурой
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    frame,
                    text="",
                    width=3,
                    height=1,
                    font=FONT_PX,
                    command=lambda rr=r, cc=c: self._move(rr, cc),
                    bg=CELL_BG,
                    activebackground=BUTTON_HOVER,
                    fg=TEXT_COLOR,
                    bd=4,
                    relief="raised",
                    highlightthickness=2,
                    highlightbackground=CELL_EDGE,
                    padx=0,
                    pady=0
                )
                btn.grid(row=r, column=c, padx=BLOCK_PAD, pady=BLOCK_PAD)
                self.grid[r][c] = btn

        # Панель управления
        control_frame = tk.Frame(self.root, bg=BG_COLOR)
        control_frame.grid(row=2, column=0, columnspan=3, pady=(5, 20))

        self.status_label = tk.Label(
            control_frame,
            text="ХОДИТ: X",
            font=("Minecraft", 14, "bold"),
            fg="#ffffff",
            bg=BG_COLOR
        )
        self.status_label.pack(side=tk.LEFT, padx=15)

        reset_btn = tk.Button(
            control_frame,
            text="НАЧАТЬ ЗАНОВО",
            command=self.reset_game,
            font=("Minecraft", 12, "bold"),
            bg=RESET_BG,
            fg="white",
            bd=3,
            relief="raised",
            padx=10,
            pady=5
        )
        reset_btn.pack(side=tk.RIGHT, padx=15)

        # Эффект наведения для кнопок
        for r in range(3):
            for c in range(3):
                btn = self.grid[r][c]
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BUTTON_HOVER))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=CELL_BG))

        self.reset_field()

    def _move(self, r, c):
        btn = self.grid[r][c]
        if btn["text"]:
            return

        btn.config(text=self.current, fg=X_COLOR if self.current == "X" else O_COLOR)
        self.moves += 1

        if self._winner(self.current):
            self.scores[self.current] += 1
            messagebox.showinfo(
                "Игра окончена",
                f"""Игрок {self.current} победил!

    Счёт: X — {self.scores['X']}, O — {self.scores['O']}"""
            )
            self._end_round()
            return

        if self.moves == 9:
            self.scores["Tie"] += 1
            messagebox.showinfo(
                "Игра окончена",
                f"""Ничья!

    Счёт: X — {self.scores['X']}, O — {self.scores['O']}, Ничьи — {self.scores['Tie']}"""
            )
            self._end_round()
            return

        self.current = "O" if self.current == "X" else "X"
        self.status_label.config(text=f"ХОДИТ: {self.current}")

    def _winner(self, symbol):
        g = self.grid
        # Проверка строк
        for i in range(3):
            if g[i][0]["text"] == g[i][1]["text"] == g[i][2]["text"] == symbol:
                return True
        # Проверка столбцов
        for i in range(3):
            if g[0][i]["text"] == g[1][i]["text"] == g[2][i]["text"] == symbol:
                return True
        # Диагонали
        if g[0][0]["text"] == g[1][1]["text"] == g[2][2]["text"] == symbol:
            return True
        if g[0][2]["text"] == g[1][1]["text"] == g[2][0]["text"] == symbol:
            return True
        return False

    def _end_round(self):
        for r in range(3):
            for c in range(3):
                self.grid[r][c]["state"] = "disabled"
        self.status_label.config(
            text=f"СЧЁТ: X — {self.scores['X']}  O — {self.scores['O']}  НИЧЬИ — {self.scores['Tie']}"
        )
        self.root.after(1800, self.reset_field)

    def reset_field(self):
        for r in range(3):
            for c in range(3):
                btn = self.grid[r][c]
                btn.config(text="", state="normal", bg=CELL_BG)
        self.moves = 0
        self.current = "X"
        self.status_label.config(text="ХОДИТ: X")

    def reset_game(self):
        self.reset_field()
        for key in self.scores:
            self.scores[key] = 0
        self.status_label.config(text="ХОДИТ: X")
        messagebox.showinfo("Начало новой игры", "Счёт обнулён. Поехали заново!")

def main():
    root = tk.Tk()
    # Установка шрифта Minecraft (если установлен в системе)
    try:
        root.option_add("*Font", "Minecraft 12")
    except:
        pass  # Если шрифт не найден, используется стандартный
        self.reset_field()


def main():
    root = tk.Tk()

    # Попытка установить шрифт Minecraft (если он есть в системе)
    try:
        # Для Windows
        root.option_add("*Font", "Minecraft 12")
    except:
        pass  # Если шрифт не найден — используем стандартный

    app = PixelStoneTicTacToe(root)

    # Настройка иконок и дополнительных стилей
    root.iconbitmap(None)  # Убираем стандартную иконку
    root.configure(bg=BG_COLOR)

    # Центрируем окно
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()