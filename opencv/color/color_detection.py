from argparse import ArgumentParser

import cv2
import pandas

# Taking an image from user
ap = ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Please input image path')
args = vars(ap.parse_args())
print(args)
img_path = args['image']

# declaring global variables (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0

# Reading image with CV
img = cv2.imread(img_path)

# Reading the csv file with pandas
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
color_csv = pandas.read_csv('colors.csv', names=index, header=None)


# Draw picked area
def draw_picked_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# Calculate distance to get color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(color_csv)):
        d = abs(R - int(color_csv.loc[i, "R"])) + abs(G - int(color_csv.loc[i, "G"])) + abs(
            B - int(color_csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = color_csv.loc[i, "color_name"]
    return cname


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_picked_color)

# Display image on the window
while True:
    cv2.imshow('image', img)
    if clicked:
        # cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        # Creating text string to display ( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        else:
            # cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        clicked = False

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
