import tkinter as tk
import math


class Julia(object):

    def __init__(self, size_x, size_y, func):
        self.size_x = size_x
        self.size_y = size_y
        self.func = func
        self.root = tk.Tk()
        self.root.title("Julia")
        self.root.geometry("{0}x{1}+200+200".format(size_x, size_y))
        self.root.overrideredirect(True)
        self.canvas = tk.Canvas(
            self.root,
            width=self.size_x - 2,
            height=self.size_y - 2,
            bd=2,
            bg="#fff")
        self.canvas.bind("<Button-1>", lambda e: self.quit())
        self.canvas.pack()

    def draw_pixel(self, x, y, color="#000"):
        self.canvas.create_line(x, y, x + 1, y + 1, fill=color, width=1)

    def start(self):
        R = (1 + math.sqrt(1 + 4 * abs(self.func(0)))) / 2
        maxiter = 8
        scale = 100
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                re = (x - self.size_x / 2) / scale
                im = (self.size_y / 2 - y) / scale
                z =  re + im * 1j
                for i in range(0, maxiter):
                    z = self.func(z)
                if abs(z) <= R:
                    self.draw_pixel(x, y, color="#800080")
        self.root.mainloop()

    def quit(self):
        self.root.destroy()


def main():
    app = Julia(800, 600, lambda z: z ** 2 - 1)
    app.start()

if __name__ == "__main__":
    main()
