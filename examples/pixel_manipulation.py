from designer import *

frog_url = 'https://cdn.pixabay.com/photo/2017/08/15/15/44/frog-2644410_960_720.png'
frog = image(frog_url, get_width()/3)
frog['scale'] = .25

@clicking
def recolor(world):
    frog = world
    pixels = get_pixels2d(frog)
    new_pixels = []
    for y, row in enumerate(pixels):
        new_pixels.append([])
        for x, color in enumerate(row):
            r, g, b = (min(255, c*1.5) for c in color[:-1])
            a = color[3]
            new_pixels[y].append((r, g, b, a))

    frog._load_image_from_list(new_pixels)
    frog._redraw_internal_image()
    #frog2 = image(new_pixels, get_width()/3 * 2)

draw(frog)
