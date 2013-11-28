import math
import gradient

def julia2(c=-0.4+0.6j, maxiter=40, size_x=800, size_y=600, offset_x=0, offset_y=0, scale=200):
    """
    Generate julia set for function f(w) = w ^ 2 + c
    Accepts:
        c: constant
        maxiter: number of iterations
        size_x: map width
        size_y: map height
        offset_x
        offset_y
        scale: scale factor
    """
    func = lambda w: w ** 2 + c
    R = (1 + math.sqrt(1 + 4 * abs(func(0)))) / 2
    colors = gradient.generate_gradient("#E1FFA2", "#470063", maxiter)
    for y in range(offset_y, size_y + offset_y):
        line = "{"
        for x in range(offset_x, size_x + offset_x):
            re = (x - size_x / 2) / scale
            im = (size_y / 2 - y) / scale
            z =  re + im * 1j
            for i in range(0, maxiter):
                z = func(z)
                if abs(z) > R:
                    break
            line += colors[i]
            if x < size_x + offset_x - 1:
                line += " "
        line += "}"
        yield y - offset_y, line
