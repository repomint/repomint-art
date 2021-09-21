from flask import Flask, render_template, request
from PIL import Image
import base64
from io import BytesIO
import requests
import numpy as np

app = Flask(__name__)

def return_image(image):
    data = BytesIO()
    image.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data

def generateRandomNumber(lowIn, highIn, sizeIn):
    rng = np.random.default_rng(42)
    ranNumberArray = rng.integers(low=lowIn, high=highIn, size=sizeIn)
    return ranNumberArray

def convert_stars(stars):
    if stars < 10:
        return 5 
    elif stars < 51:
        return 10
    elif stars < 1001:
        return 15
    else:
        return 20

def generate_image(yel_stars,r=250,g=250,b=250):
    #generate background color
    first_im = Image.new(mode="RGBA", size=(300, 300), color = (r,g,b))

    #get star image        
    star_url='https://cdn.pixabay.com/photo/2017/01/07/21/22/stars-1961613_1280.png'
    img = requests.get(star_url).content
    #preprocess star image
    team_img = Image.open(BytesIO(img)).convert("RGBA")
    team_img = team_img.resize((40, 20), resample=Image.NEAREST)

    #generate the location of stars *2 for x and y axis
    hor = generateRandomNumber(0,280,yel_stars*2)
    #put on the image
    for x in range(yel_stars):
        first_im.paste(team_img,(hor[x],hor[x+yel_stars]), team_img)
    return first_im

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route('/art', methods=['POST'])
def generate_art():

    #get data from the form
    data = [x for x in request.form.values()]
    pic_team = data[0]

    if data[1].isdigit():
        stars = int(data[1])
    else:
        stars = 0
        
    if data[2].isdigit():
        r = int(data[2])
    else:
        r = 250
    if data[3].isdigit():
        g = int(data[3])
    else:
        g=250
    if data[4].isdigit():
        b = int(data[4])
    else:
        b=250

    #convert stars number
    yel_stars = convert_stars(stars)
    first_im=generate_image(yel_stars, r, g, b)

    #request for the image from url
    pic_team = requests.get(pic_team).content
    
    #preprocess image
    team_img = Image.open(BytesIO(pic_team)).convert("RGBA")
    team_img = team_img.resize((200, 200), resample=Image.NEAREST)
    first_im.paste(team_img,(50,0), team_img)

    #pass image to the user
    img_data = return_image(first_im)

    return render_template("art.html", img_data=img_data.decode('utf-8'))
