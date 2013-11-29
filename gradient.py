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


def simple_gradient(color1, color2, n):
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
    for i in range(0, n):
        hi = hsv1[0] + i * h_step
        si = hsv1[1] + i * s_step
        vi = hsv1[2] + i * v_step
        code = rgb256_to_code(*rgb_to_rgb256(*colorsys.hsv_to_rgb(hi, si, vi)))
        yield code

def create_gradient(col_table, total_steps):
    """
    Accepts:
        col_table: (x, color) pairs
        total_steps: total number of divisions
    """
    col_table.sort(key=lambda c: c[0])
    d = col_table[-1][0] - col_table[0][0]
    # Find gradient parts
    parts = []
    for i in range(0, len(col_table) - 1):
        br1, col1 = col_table[i]
        br2, col2 = col_table[i + 1]
        share = total_steps * (br2 - br1) / d
        parts.append({
            'col1': col1,
            'col2': col2,
            'int': math.floor(share),
            'rem': share - math.floor(share),
        })
    # Allocate free steps using largest remainder method
    free_steps = total_steps - sum(p['int'] for p in parts)
    for part in sorted(parts, key=lambda p: p['rem'], reverse=True):
        part['int'] += 1
        free_steps -= 1
        if free_steps == 0:
            break
    # Get color codes for each part
    gradient = []
    for part in parts:
        for code in simple_gradient(part['col1'], part['col2'], part['int']):
            gradient.append(code)
    return gradient
