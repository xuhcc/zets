import math

def generate_set(func, size_x, size_y, scale, maxiter):
    R = (1 + math.sqrt(1 + 4 * abs(func(0)))) / 2
    for x in range(0, size_x):
        for y in range(0, size_y):
            re = (x - size_x / 2) / scale
            im = (size_y / 2 - y) / scale
            z =  re + im * 1j
            for i in range(0, maxiter):
                z = func(z)
                if abs(z) > R:
                    break
            yield (x, y, i)
