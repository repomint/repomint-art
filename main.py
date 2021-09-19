from flask import Flask, render_template, request
from PIL import Image, ImageDraw
import base64
import io


app = Flask(__name__)

@app.route('/')
def background():
    if request.args.get('r',''):
        r = int(request.args.get('r',''))
    else:
        r=255
    if request.args.get('g',''):
        g = int(request.args.get('g',''))
    else:
        g=0
    if request.args.get('b',''):
        b = int(request.args.get('b',''))
    else:
        b=0

    im = Image.new(mode="RGB", size=(400, 400), color = (r,g,b))

    draw = ImageDraw.Draw(im)
    #draw.ellipse((100, 100, 150, 200), fill=(255, 0, 0), outline=(0, 0, 0))
    draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    #im.paste()
    data = io.BytesIO()
    im.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("index.html", img_data=encoded_img_data.decode('utf-8'))