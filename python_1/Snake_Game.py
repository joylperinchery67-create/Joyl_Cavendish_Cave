#!/usr/bin/env python3
"""Simple Snake game using Tkinter.

Controls:
  - Arrow keys or WASD to move
  - R to restart after game over

This is self-contained and requires only the Python standard library (Tkinter).
"""
import random
import tkinter as tk
from typing import List, Tuple


Cell = Tuple[int, int]


class SnakeGame:
    def __init__(self, master: tk.Tk, width=600, height=400, cell_size=20):
        self.master = master
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size

        self.canvas = tk.Canvas(master, width=width, height=height, bg="#111")
        self.canvas.pack()

        self.score_var = tk.IntVar(value=0)
        self.score_label = tk.Label(master, textvariable=self.score_text(), font=("Helvetica", 12))
        self.score_label.pack(side=tk.LEFT, padx=8)

        self.info_label = tk.Label(master, text="Arrows / WASD to play — R to restart", font=("Helvetica", 10))
        self.info_label.pack(side=tk.RIGHT, padx=8)

        self.reset()
        self.bind_keys()

    def score_text(self):
        # returns a tk.StringVar-like wrapper (score_var is IntVar, but Label accepts textvariable)
        return self.score_var

    def reset(self):
        # Initial snake in the middle, horizontal moving right
        mid_x = self.cols // 2
        mid_y = self.rows // 2
        self.snake: List[Cell] = [(mid_x - i, mid_y) for i in range(3)]
        self.direction = (1, 0)  # moving right
        self.next_direction = self.direction
        self.place_food()
        self.game_over = False
        self.speed = 120  # milliseconds between moves
        self.score_var.set(0)
        self.redraw()
        # Start the loop
        self.master.after(self.speed, self.tick)

    def bind_keys(self):
        self.master.bind("<Up>", lambda e: self.change_direction((0, -1)))
        self.master.bind("<Down>", lambda e: self.change_direction((0, 1)))
        self.master.bind("<Left>", lambda e: self.change_direction((-1, 0)))
        self.master.bind("<Right>", lambda e: self.change_direction((1, 0)))
        # WASD
        self.master.bind("w", lambda e: self.change_direction((0, -1)))
        self.master.bind("s", lambda e: self.change_direction((0, 1)))
        self.master.bind("a", lambda e: self.change_direction((-1, 0)))
        self.master.bind("d", lambda e: self.change_direction((1, 0)))
        self.master.bind("r", lambda e: self.on_restart())

    def change_direction(self, d: Cell):
        # Prevent reversing directly
        if (d[0] == -self.direction[0] and d[1] == -self.direction[1]):
            return
        self.next_direction = d

    def place_food(self):
        empty_cells = [(x, y) for x in range(self.cols) for y in range(self.rows) if (x, y) not in self.snake]
        self.food = random.choice(empty_cells) if empty_cells else None

    def tick(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.cols, (head_y + dy) % self.rows)

        # Collision with self?
        if new_head in self.snake:
            self.on_game_over()
            return

        self.snake.insert(0, new_head)

        # Eating food?
        if self.food and new_head == self.food:
            self.score_var.set(self.score_var.get() + 1)
            # speed up a bit
            self.speed = max(30, int(self.speed * 0.95))
            self.place_food()
        else:
            # remove tail
            self.snake.pop()

        self.redraw()
        self.master.after(self.speed, self.tick)

    def redraw(self):
        self.canvas.delete("all")

        # draw food
        if self.food:
            x, y = self.food
            self._draw_cell(x, y, fill="#e74c3c")

        # draw snake
        for i, (x, y) in enumerate(self.snake):
            color = "#2ecc71" if i == 0 else "#27ae60"
            self._draw_cell(x, y, fill=color)

        # optional grid lines (comment out for a cleaner look)
        # for i in range(self.cols + 1):
        #     self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.height, fill="#222")
        # for j in range(self.rows + 1):
        #     self.canvas.create_line(0, j * self.cell_size, self.width, j * self.cell_size, fill="#222")

    def _draw_cell(self, grid_x: int, grid_y: int, fill="#fff"):
        x1 = grid_x * self.cell_size
        y1 = grid_y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        pad = max(1, self.cell_size // 10)
        self.canvas.create_rectangle(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill=fill, outline="" )

    def on_game_over(self):
        self.game_over = True
        self.canvas.create_text(self.width // 2, self.height // 2 - 20, text="GAME OVER", fill="#fff", font=("Helvetica", 24, "bold"))
        self.canvas.create_text(self.width // 2, self.height // 2 + 14, text=f"Score: {self.score_var.get()}", fill="#ddd", font=("Helvetica", 14))
        self.canvas.create_text(self.width // 2, self.height // 2 + 44, text="Press R to restart", fill="#aaa", font=("Helvetica", 10))

    def on_restart(self):
        if self.game_over:
            self.reset()


def main():
    root = tk.Tk()
    root.title("Snake — Tkinter")
    game = SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
