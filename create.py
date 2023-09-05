import os
from tkinter import YES, BOTH
import tkinter
import PIL.Image, PIL.ImageDraw
import operator

lastPoint = None

width = 200  # canvas width
height = 200 # canvas height
black = (255, 255) # pen color
white = (0, 255) # canvas back
penWidth = 7

validRectObj = None
validRect = (width, height, 0, 0)

sample_img_size = 28

def save():
    # crop image
    global validRect
    validW = validRect[2] - validRect[0]
    validH = validRect[3] - validRect[1]
    if validW > validH:
        validRect = (validRect[0], validRect[1] - (validW - validH)//2, validRect[2], validRect[3] + (validW - validH)//2)
    else:
        validRect = (validRect[0] - (validH - validW)//2, validRect[1], validRect[2] + (validH - validW)//2, validRect[3])
    margin = 4 * (100 // 28) + penWidth
    validRect = tuple(map(operator.sub, validRect, (margin, margin, -margin, -margin)))

    newimg = output_image.crop(validRect).resize((sample_img_size, sample_img_size), PIL.Image.LINEAR)
    newimg.convert("RGB").save("user_image_hw.jpg")
def clear():
    global lastPoint
    global validRect
    global validRectObj
    lastPoint = None
    validRect = (width, height, 0, 0)
    validRectObj = None
    canvas.delete("all")
    draw.rectangle((0, 0, width, height), white)

def buttonRelease(event):
    global lastPoint
    lastPoint = None

def buttonMotion(event):
    global lastPoint
    global validRect
    global validRectObj
    if lastPoint is not None:
        last_x = lastPoint[0]
        last_y = lastPoint[1]
        canvas.create_line(last_x, last_y, event.x, event.y, fill="black", width = penWidth)
        draw.line([last_x, last_y, event.x, event.y], fill=black, width = penWidth)
    lastPoint = (event.x, event.y)
    validRect = (min(validRect[0], event.x), min(validRect[1], event.y),max(validRect[2], event.x), max(validRect[3], event.y))
    if validRectObj is not None:
        canvas.delete(validRectObj)
    validRectObj = canvas.create_rectangle(validRect)


master = tkinter.Tk()

# create a tkinter canvas to draw on
canvas = tkinter.Canvas(master, width=width, height=height, bg='white')
canvas.pack()

# create an empty PIL image and draw object to draw on
output_image = PIL.Image.new("LA", (width, height), color = white)
draw = PIL.ImageDraw.Draw(output_image)
canvas.pack(expand=YES, fill=BOTH)
canvas.bind("<B1-Motion>", buttonMotion)
canvas.bind("<ButtonRelease-1>", buttonRelease)

# add a button to save the image
btn_save = tkinter.Button(text="Save",command=save)
btn_save.pack()

# add a button to save the image
btn_clear = tkinter.Button(text="clear",command=clear)
btn_clear.pack()

master.mainloop()