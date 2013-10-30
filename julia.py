import tkinter as tk
import math

colors = [
    "#EFE6FF",
    "#DCCCFF",
    "#C7B3FF",
    "#B199FF",
    "#9980FF",
    "#7F66FF",
    "#644CFF",
    "#3019FF",
    "#EFE6FF",
    "#DCCCFF",
    "#C7B3FF",
    "#B199FF",
    "#9980FF",
    "#7F66FF",
    "#644CFF",
    "#3019FF",
    "#EFE6FF",
    "#DCCCFF",
    "#C7B3FF",
    "#B199FF",
    "#9980FF",
    "#7F66FF",
    "#644CFF",
    "#3019FF",
    "#EFE6FF",
    "#DCCCFF",
    "#C7B3FF",
    "#B199FF",
    "#9980FF",
    "#7F66FF",
    "#644CFF",
    "#3019FF",
]


class Julia(object):

    def __init__(self, size_x, size_y, func):
        self.size_x = size_x
        self.size_y = size_y
        self.func = func
        self.root = tk.Tk()
        self.root.title("Julia")
        self.root.geometry("{0}x{1}+200+200".format(size_x + 2, size_y + 2))
        self.root.overrideredirect(True)
        self.canvas = tk.Canvas(
            self.root,
            width=self.size_x,
            height=self.size_y,
            bd=2,
            bg=colors[0])
        self.canvas.bind("<Button-1>", lambda e: self.quit())
        self.canvas.pack()
        self.root.after(50, self.generate_set)

    def draw_pixel(self, x, y, color="#000"):
        self.canvas.create_line(x, y, x + 1, y + 1, fill=color, width=1)

    def generate_set(self):
        R = (1 + math.sqrt(1 + 4 * abs(self.func(0)))) / 2
        maxiter = 20
        scale = 200
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                re = (x - self.size_x / 2) / scale
                im = (self.size_y / 2 - y) / scale
                z =  re + im * 1j
                for i in range(0, maxiter):
                    z = self.func(z)
                    if abs(z) > R:
                        break
                if 0 < i < maxiter:
                    self.draw_pixel(x, y, color=colors[i])

    def start(self):
        self.root.mainloop()

    def quit(self):
        self.root.destroy()


def main():
    c = -0.4 + 0.6j
    app = Julia(800, 600, lambda z: z ** 2 + c)
    app.start()

if __name__ == "__main__":
    main()
