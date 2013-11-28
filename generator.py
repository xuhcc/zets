import math
import gradient

def julia2(c=-0.4+0.6j, maxiter=40, size_x=800, size_y=600, offset_x=0, offset_y=0, zoom=1):
    """
    Generate Julia set for function f(z) = z ^ 2 + c
    Accepts:
        c: constant
        maxiter: number of iterations
        size_x: map width (pixels)
        size_y: map height (pixels)
        offset_x: x offset (pixels)
        offset_y: y offset (pixels)
        zoom: magnification level
    """
    func = lambda z: z ** 2 + c
    R = (1 + math.sqrt(1 + 4 * abs(func(0)))) / 2
    colors = gradient.generate_gradient("#E1FFA2", "#470063", maxiter)
    # Calculate scale
    # Height 600 and zoom 1 translates into -2 < Im z < 2
    scale = (size_y / 600) * (zoom * 150)
    offset_x = offset_x * zoom
    offset_y = offset_y * zoom
    for y in range(0, size_y):
        line = "{"
        for x in range(0, size_x):
            re = ((x + offset_x) - size_x / 2) / scale
            im = (size_y / 2 - (y + offset_y)) / scale
            z =  re + im * 1j
            for i in range(0, maxiter):
                z = func(z)
                if abs(z) > R:
                    break
            line += colors[i]
            if x < size_x - 1:
                line += " "
        line += "}"
        yield y, line

def mandelbrot(maxiter=40, size_x=600, size_y=600, offset_x=0, offset_y=0, zoom=1):
    """
    Generate Mandelbrot set
    Accepts:
        maxiter: number of iterations
        size_x: map width (pixels)
        size_y: map height (pixels)
        offset_x: x offset (pixels)
        offset_y: y offset (pixels)
        zoom: magnification level
    """
    func = lambda z, c: z ** 2 + c
    R = 2
    colors = gradient.generate_gradient("#E1FFA2", "#470063", maxiter)
    # Calculate scale
    # Height 600 and zoom 1 translates into -2.5 < Im c < 2.5
    scale = (size_y / 600) * (zoom * 120)
    offset_x = offset_x * zoom
    offset_y = offset_y * zoom
    for y in range(0, size_y):
        line = "{"
        for x in range(0, size_x):
            re = ((x + offset_x) - size_x / 2) / scale
            im = (size_y / 2 - (y + offset_y)) / scale
            c =  re + im * 1j
            z = 0
            for i in range(0, maxiter):
                z = func(z, c)
                if abs(z) > R:
                    break
            line += colors[i]
            if x < size_x - 1:
                line += " "
        line += "}"
        yield y, line
