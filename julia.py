import tkinter as tk
import math
import colorsys

def hsv360_to_hsv(h, s, v):
    """
    Hue:        0...360
    Saturation: 0...100
    Value:      0...100
    """
    h_ = h / 360
    s_ = s / 100
    v_ = v / 100
    return h_, s_, v_

def rgb_to_rgb256(r, g, b):
    r_ = math.floor(r * 255)
    g_ = math.floor(g * 255)
    b_ = math.floor(b * 255)
    return r_, g_, b_

def rgb256_to_code(r, g, b):
    hexr = hex(r)[2:].zfill(2)
    hexg = hex(g)[2:].zfill(2)
    hexb = hex(b)[2:].zfill(2)
    code = "#" + hexr + hexg + hexb
    return code

def generate_gradient(color1, color2, r):
    hsv1 = hsv360_to_hsv(*color1)
    hsv2 = hsv360_to_hsv(*color2)
    h_step = (hsv2[0] - hsv1[0]) / r
    s_step = (hsv2[1] - hsv1[1]) / r
    v_step = (hsv2[2] - hsv1[2]) / r
    gradient = []
    for i in range(0, r):
        hsv = (hsv1[0] + i * h_step, hsv1[1] + i * s_step, hsv1[2] + i * v_step)
        rgb = colorsys.hsv_to_rgb(*hsv)
        code = rgb256_to_code(*rgb_to_rgb256(*rgb))
        gradient.append(code)
    return gradient


class Julia(object):

    def __init__(self, size_x, size_y, func, maxiter, scale):
        self.size_x = size_x
        self.size_y = size_y
        self.func = func
        self.maxiter = maxiter
        self.scale = scale
        self.colors = generate_gradient(
            (290, 10, 100),
            (250, 100, 100),
            self.maxiter)
        self.root = tk.Tk()
        self.root.title("Julia")
        self.root.geometry("{0}x{1}+200+150".format(size_x + 2, size_y + 2))
        self.root.overrideredirect(True)
        self.canvas = tk.Canvas(
            self.root,
            width=self.size_x,
            height=self.size_y,
            bd=2,
            bg=self.colors[0])
        self.canvas.bind("<Button-1>", lambda e: self.quit())
        self.canvas.pack()
        self.root.after(50, self.generate_set)

    def draw_pixel(self, x, y, color="#000"):
        self.canvas.create_line(x, y, x + 1, y + 1, fill=color, width=1)

    def generate_set(self):
        R = (1 + math.sqrt(1 + 4 * abs(self.func(0)))) / 2
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                re = (x - self.size_x / 2) / self.scale
                im = (self.size_y / 2 - y) / self.scale
                z =  re + im * 1j
                for i in range(0, self.maxiter):
                    z = self.func(z)
                    if abs(z) > R:
                        break
                if 0 < i < self.maxiter:
                    self.draw_pixel(x, y, color=self.colors[i])

    def start(self):
        self.root.mainloop()

    def quit(self):
        self.root.destroy()


def main():
    func = lambda z: z ** 2 - 0.4 + 0.6j
    app = Julia(1000, 800, func, 100, 250)
    app.start()

if __name__ == "__main__":
    main()
