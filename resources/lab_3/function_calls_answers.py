from designer import *

# set background color
set_window_color('lightgreen')

# FIRST EMOJI (SMILE)
# make face
smile_face = circle('lightyellow', 100, 100, 300)

# make eyes
s_right_eye = circle('black', 10, 150, 275)
s_left_eye = circle('black', 10, 50, 275)

# Make mouth (mouth example with arc)
s_mouth = arc('red', (3.14* 3)/4, 3.14/4, 5, 50, 340, 100, 20)

# group emoji 1 (OPTIONAL - Especially good code style)
smile = group(smile_face, s_right_eye, s_left_eye, s_mouth)

# SECOND EMOJI (FROWN):
# make face
frown_face = circle('lightyellow', 100, 400, 300)

# make eyes
f_right_eye = circle('black', 10, 450, 275)
f_left_eye = circle('black', 10, 350, 275)

# make mouth (mouth example with lines)
mouth_1 = line('red', 5, 340, 370, 350, 340)
mouth_2 = line('red', 5, 350, 340, 450, 340)
mouth_3 = line('red', 5, 450, 340, 460, 370)

f_mouth = group(mouth_1, mouth_2, mouth_3)

# group emoji 2 (OPTIONAL - Especially good code style)
frown = group(frown_face, f_right_eye, f_left_eye, f_mouth)

# THIRD EMOJI:
# make face
angry_face = circle('lightyellow', 100, 700, 300)

# make eyes
a_right_eye = circle('black', 10, 750, 275)
a_left_eye = circle('black', 10, 650, 275)

# make eyebrows
a_right_eyebrow = line('black', 2, 725, 265, 770, 250)
a_left_eyebrow = line('black', 2, 675, 265, 630, 250)

# make mouth
a_mouth = circle('black', 20, 700, 350)

#EXTRA CREDIT, GROUPING
angry = group(angry_face, a_right_eye, a_left_eye, a_right_eyebrow, a_left_eyebrow, a_mouth)
# glide_down(emoji, 1)


draw(smile, frown, angry)
'''
How many function calls are there?
There are 4 function calls
 
 For at least two function calls: 
 1. Explain what the function does (What is its purpose?) 
 2. Note any arguments and what the arguments represent  
 3. Identify the return value
 You should answer 1-3 for at least 2 function calls.
 
set_window_color: 
 1. sets the background color of the window. 
 2. Takes 1 argument, the color to set the background
 3. Returns None
 
circle: 
1. Creates a circle to draw on the screen 
2. Takes 4 arguments: the first is the radius of the circle to be drawn as an int, then the color of the circle,
then the x position of the center of the circle on the window as an int, then the y position of the center of the
circle on the window as an int 
3. Returns the circle created

glide_left: 
1. Moves the given parameter to the left on the window
2. Takes 2 arguments, the object to be moved and the speed at which to move it 
3. Returns None

draw: 
1. Starts the window and all actions
2. Does not take any arguments
3. Returns None   


'''