from fumen.decoder import decode
from fumen.defines import Piece
import tkinter as tk

class App(tk.Tk):
    # 20 buffer on all sides
    # 30 cell size
    
    def __init__(self, filename: str):
        super().__init__()
        self.fumens = self.read_fumens(filename)
        self.fumen_index = 0 
        self.pages = []     # all the pages loaded in the fumen
        self.cells = []     # array of 23x10 rectangles
        self.index = 0      # which page currently showing
        self.n = 0          # how many pages
        self.canvas = tk.Canvas(self, width=340, height=730)
        self.canvas.pack()

        self.bind('<Key>', self.key_pressed)
        self.bind('<Return>', self.return_key)
        self.entry = tk.Entry(self)
        self.entry.place(x=10, y=0)
        self.init_board()

    def return_key(self, _):
        self.fumen_index = int(self.entry.get())
        self.entry.delete(0, tk.END)
        print("Displaying", self.fumens[self.fumen_index])
        self.setup()
        
    def key_pressed(self, event):
        if event.keycode == 113: # left
            self.index = max(0, self.index - 1)
            self.update_board()
        elif event.keycode == 114: # right
            self.index = min(self.n - 1, self.index + 1)
            self.update_board()

    def update_board(self):
        colors = ['#313456', '#53ceab', '#ce8053', '#cfc552', '#ce525a', '#c352ce', '#6652ce', '#80ce52', '#313456']
        field = self.pages[self.index].get_field().get_board()
        for row in range(23):
            for col in range(10):
                cell_id = self.cells[row][col]
                piece = field[22 - row][col]
                color = colors[piece.value]
                self.canvas.itemconfig(cell_id, fill=color)

    def init_board(self):
        self.cells = [
            [self.canvas.create_rectangle(*self.get_coords(row, col))
             for col in range(10)]
            for row in range(23)
        ]

    def get_coords(self, row, col) -> list[int]:
        # returns the two corners of the cell
        y1, y2 = (23 - row) * 30, (22 - row) * 30
        x1, x2 = col * 30, col * 30 + 30
        return [x1 + 20, y1 + 20, x2 + 20, y2 + 20]
    
    def setup(self): 
        fumen = self.fumens[self.fumen_index]
        self.pages = decode(fumen)
        self.n = len(self.pages)
        self.update_board()

    def read_fumens(self, filename: str):
        with open(filename) as f:
            return f.readlines()

    def display(self):
        try:
            while self.state():
                self.update()
                self.update_idletasks()
        except tk.TclError:
            print("Exiting...")


def main():
    app = App("fumens.txt")
    app.display()

if __name__ == "__main__":
    main()
