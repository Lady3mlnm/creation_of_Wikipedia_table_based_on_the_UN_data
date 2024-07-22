import math

def hsl_to_rgb(h, s, l):
    h /= 360.0
    s /= 100.0
    l /= 100.0
    
    if s == 0:
        r = g = b = l  # achromatic
    else:
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p
        
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return int(r * 255), int(g * 255), int(b * 255)


def hsl_to_hex(h, s, l):
    rgb = hsl_to_rgb(h, s, l)
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def number_to_hex(number, max_number, palette_type=None, hue=None, saturation=None, lighness_fn=None, log=False):
    '''
    The function assign to value some color depending on retalion this value to maximum value.
    number: int or float
    max_number: int or float
    palette_type: 'blue', 'indigo' or None
        This parameter allows to with one input determine hue, saturation and lighness_fn. So that a user don't recall their specific values.
    hue: int or float
        Hue for manual input.
    saturation: int or float
        Saturation for manual input.
    lighness_fn: function
        Function for manual input or correction standard function for 'blue' and 'indigo' palettes. It should be in the form
        lambda n, max_n: <saturation_start> - <delta> * fn(n, max_n)
        The lower difference (100 - start argument) the lighter lowest value.
        The lower difference (start argument - change_ratio) the darker highest value.
    log: bool
        This parameter makes sence only with given palette_type. It determine whether scale is linear or logarithmic. This is modification of function lighness_fn for given palette_type.
    return: string
        String, representing color in the RGB form, like "#ffff00" for yellow, "#ff00ff" for magenta/fuchsia, #00ffff" for aqua/cyan.
    '''
    
    if palette_type=='blue':
        hue, saturation = (202, 53)
        if not lighness_fn:
            if not log:
                lighness_fn = lambda n, max_n: 84 - 54 * n / max_n
            else:
                lighness_fn = lambda n, max_n: 84 - 54 * math.log(n+1) / math.log(max_n+1)
    elif palette_type=='indigo':
        hue, saturation = (242, 42)
        if not lighness_fn:
            if not log:
                lighness_fn = lambda n, max_n: 100 - 74 * n / max_n
            else:
                lighness_fn = lambda n, max_n: 100 - 74 * math.log(n+1) / math.log(max_n+1)
                
    lightness = lighness_fn(number, max_number)
    
    return hsl_to_hex(hue, saturation, lightness)   # (hue, saturation, round(lightness, 3))