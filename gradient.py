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

def rgb256_to_rgb(r, g, b):
    """
    Red:    0...255
    Green:  0...255
    Blue:   0...255
    """
    r_ = r / 255
    g_ = g / 255
    b_ = b / 255
    return r_, g_, b_

def rgb256_to_code(r, g, b):
    hexr = hex(r)[2:].zfill(2)
    hexg = hex(g)[2:].zfill(2)
    hexb = hex(b)[2:].zfill(2)
    code = "#" + hexr + hexg + hexb
    return code

def code_to_rgb256(code):
    r = int(code[1:3], 16)
    g = int(code[3:5], 16)
    b = int(code[5:7], 16)
    return r, g, b


def generate_gradient(color1, color2, n):
    """
    Accepts:
        color1, color2: color codes (strings)
        n: number of divisions
    """
    hsv1 = colorsys.rgb_to_hsv(*rgb256_to_rgb(*code_to_rgb256(color1)))
    hsv2 = colorsys.rgb_to_hsv(*rgb256_to_rgb(*code_to_rgb256(color2)))
    h_step = (hsv2[0] - hsv1[0]) / n
    s_step = (hsv2[1] - hsv1[1]) / n
    v_step = (hsv2[2] - hsv1[2]) / n
    gradient = []
    for i in range(0, n):
        hi = hsv1[0] + i * h_step
        si = hsv1[1] + i * s_step
        vi = hsv1[2] + i * v_step
        code = rgb256_to_code(*rgb_to_rgb256(*colorsys.hsv_to_rgb(hi, si, vi)))
        gradient.append(code)
    return gradient
