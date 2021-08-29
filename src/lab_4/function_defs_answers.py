from designer import *
'''
# LAB 3 CODE: 
# set background color
set_window_color('lightgreen')

# make face
face = circle('lightyellow', 100, 400, 300)

# make eyes
right_eye = circle('black', 10, 450, 275)
left_eye = circle('black', 10, 350, 275)

# make eyebrows
right_eyebrow = line(2, 'black', 425, 265, 470, 250)
left_eyebrow = line(2, 'black', 375, 265, 330, 250)

# make mouth
mouth = circle('black', 20, 400, 350)

#EXTRA CREDIT, GROUPING
emoji = group(face, right_eye, left_eye, right_eyebrow, left_eyebrow, mouth)
glide_down(emoji, 1)


draw()
'''

def shocked_emoji(mouth_size, eye_color, center_face_x, center_face_y):
    face = circle('lightyellow', 100, center_face_x, center_face_y)
    right_eye = circle(eye_color, 10, center_face_x + 50, center_face_y - 25)
    left_eye = circle(eye_color, 10, center_face_x - 50, center_face_y - 25)
    mouth = circle('black', mouth_size, center_face_x, center_face_y + 50)
    emoji = group(face, right_eye, left_eye, mouth)
    return emoji

set_window_color('lightgreen')

blue_eye_small_mouth_emoji = shocked_emoji(20, 'blue', 125, 150)
green_eye_small_mouth_emoji = shocked_emoji(20, 'green', 375, 150)
brown_eye_small_mouth_emoji = shocked_emoji(20, 'brown', 625, 150)


blue_eye_big_mouth_emoji = shocked_emoji(30, 'blue', 125, 400)
green_eye_big_mouth_emoji = shocked_emoji(30, 'green', 375, 400)
brown_eye_big_mouth_emoji = shocked_emoji(30, 'brown', 625, 400)



draw(blue_eye_small_mouth_emoji, green_eye_small_mouth_emoji, brown_eye_small_mouth_emoji, blue_eye_big_mouth_emoji,
     green_eye_big_mouth_emoji, brown_eye_big_mouth_emoji)

