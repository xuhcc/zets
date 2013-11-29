import math

import gradient

class Julia(object):
    """
    Iterator for Julia set
    """
    def __init__(self, maxiter, func=None):
        self.maxiter = maxiter
        if func is None:
            self.func = lambda z: z ** 2 - 0.4 + 0.6j
            self.r = (1 + math.sqrt(1 + 4 * abs(self.func(0)))) / 2
        else:
            self.func = func
            self.r = 1

    def __call__(self, z):
        for i in range(0, self.maxiter):
            z = self.func(z)
            if abs(z) > self.r:
                break
        return i


class Mandelbrot(object):
    """
    Iterator for Mandelbrot set
    """
    def __init__(self, maxiter):
        self.maxiter = maxiter
        self.func = lambda z, c: z ** 2 + c

    def __call__(self, c):
        z = 0
        for i in range(0, self.maxiter):
            z = self.func(z, c)
            if abs(z) > 2:
                break
        return i


def draw_map(
        mode="julia", maxiter=100,
        size_x=600, size_y=600, offset_x=0, offset_y=0, zoom=1,
        **kwargs):
    """
    Generate image map
    Accepts:
        mode: set type
        maxiter: number of iterations
        size_x: map width (pixels)
        size_y: map height (pixels)
        offset_x: x offset (pixels)
        offset_y: y offset (pixels)
        zoom: magnification level
    """
    # Choose iterator
    if mode == "julia":
        iterator = Julia(maxiter, kwargs.get('func'))
    elif mode == "mandelbrot":
        iterator = Mandelbrot(maxiter)
    # Calculate scale
    # Height 600 and zoom 1 translates into -3 < Im z < 3
    scale = (size_y / 600) * (zoom * 100)
    offset_x = offset_x * zoom
    offset_y = offset_y * zoom
    colors = gradient.generate_gradient("#CAE6FF", "#460063", maxiter)
    for y in range(0, size_y):
        line = "{"
        for x in range(0, size_x):
            re = ((x + offset_x) - size_x / 2) / scale
            im = (size_y / 2 - (y + offset_y)) / scale
            i = iterator(re + im * 1j)
            line += colors[i]
            if x < size_x - 1:
                line += " "
        line += "}"
        yield y, line
