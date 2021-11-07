from designer import *

frog_url = 'https://cdn.pixabay.com/photo/2017/08/15/15/44/frog-2644410_960_720.png'
frog = image(frog_url, 0, get_height()/2, anchor='midleft')
frog['scale'] = .25
glide_right(frog, 60)

bouncing = image(frog_url)
bouncing['scale'] = .25
glide_around(bouncing, 1)

draw(frog, bouncing)